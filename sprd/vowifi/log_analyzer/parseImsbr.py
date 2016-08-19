#Try to analysis the handover related problems. But I'm not clever enough as you
#expected, so need your help to let me know more things :(
#
#Author: liping.zhang@spreadtrum.com

from __future__ import division
import logging
import operator
import sys
import re

def compose_dict(time, lineno, msg, loglevel = logging.INFO):
	return {
		"issip" : 0,
		"isimsbr" : 1,
		"timestamp" : time,
		"lineno" : lineno,
		"msg" : msg,
		"loglevel" : loglevel,
	}

class imsbr_parser:
	def __init__(self):
		# Reg pattern:
		self.patterns = {}

		# Packets and other error statistics
		self.pkts_fromcp = 0
		self.pkts_tocp = 0
		self.sipc_fails = 0
		self.output_fails = 0

		# Tuple infos
		self.volte_tuples = 0
		self.vowifi_tuples = 0

		# Handover stat:
		self.last_ho = "ho-finish"

		self.results = []

	def search_pattern(self, name, line, regex):
		if name not in self.patterns:
			self.patterns[name] = re.compile(regex)
		return self.patterns[name].search(line)

	def add_result(self, res):
		self.results.append(res)

	def clear_stat(self):
		self.pkts_fromcp = 0
		self.pkts_tocp = 0
		self.sipc_fails = 0
		self.output_fails = 0

	def parse_tuple(self, lineno, time, line):
		'''
		Format:
		c2 imsbr: volte-add(sip) l3=41 l4=50 fd00:0:5:1::1 0 -> fd00:0:20:1::20 0	
		'''
		match = self.search_pattern("tuple", line, "imsbr: (volte|vowifi)-(add|del)(.*)")
		if not match:
			return False

		if match.group(2) == "add":
			op = operator.add
		else:
			op = operator.sub

		if match.group(1) == "volte":
			self.volte_tuples = op(self.volte_tuples, 1)
		else:
			self.vowifi_tuples = op(self.vowifi_tuples, 1)

		msg = match.group(1) + "-" + match.group(2) + match.group(3)
		self.add_result(compose_dict(time, lineno, msg))
		return True

	def parse_calls(self, lineno, time, line):
		'''
		Format:
		c0 imsbr: call switch to [volte] init=volte curr=volte ho=ho-finish->ho-finish
		'''
		match = self.search_pattern("calls", line, "imsbr: call switch to \[(.*)\]")
		if not match:
			return False

		msg = "Start " + match.group(1) + " call"
		self.add_result(compose_dict(time, lineno, msg))
		return True

	def parse_sipcfail(self, lineno, time, line):
		'''
		Format:
		c2 imsbr: sblock_send ... fail, error=-1	
		'''
		match = self.search_pattern("sipcfail", line, "(imsbr: sblock.*error.*)")
		if not match:
			return False

		self.sipc_fails += 1
		self.add_result(compose_dict(time, lineno, match.group(1)))
		return True
	
	def parse_outfail(self, lineno, time, line):
		'''
		Format:
		ip_route_output_key s=%pI4 d=%pI4 e=%ld\n
		ip_local_out s=%pI4 d=%pI4 p=%d err=%d\n
		ip6_route_output s=%pI6c d=%pI6c e=%d\n
		xfrm_lookup s=%pI6c d=%pI6c p=%d e=%ld\n
		ip6_local_out s=%pI6c d=%pI6c p=%d e=%d\n
		
		imsbr_packet_output_v6: 224 callbacks suppressed
		imsbr_packet_output: 224 callbacks suppressed
		'''

		match = self.search_pattern("outfail", line, 
			"imsbr: (ip_route_output_key|ip_local_out|ip6_route_output|xfrm_lookup|ip6_local_out).*(e|err)=")
		if match:
			self.output_fails += 1
		else:
			match = self.search_pattern("outfail2", line, 
					"imsbr_packet_output(_v6)?: (\d+) callbacks suppressed")
			if not match:
				return False
			self.output_fails += int(match.group(2))
		
		return True

	def parse_packet(self, lineno, time, line):
		'''
		Format:
		c0 imsbr: process packet from cp: src=2405:204:1a09:c645::9f7:e8b0 dst=2405:200:330:1587::10 ...
		c0 imsbr: relay packet to cp: src=2405:200:330:1587::10 dst=2405:204:1a09:c645::9f7:e8b0 ...
		
		c0 imsbr_process_packet: 304 callbacks suppressed
		c0 imsbr_packet_relay2cp: 304 callbacks suppressed
		'''
		match = self.search_pattern("packet", line, "imsbr: (process|relay) packet (from|to) cp:")

		if match:
			if match.group(1) == "process":
				self.pkts_fromcp += 1
			else:
				self.pkts_tocp += 1
		else:
			match = self.search_pattern("packet2", line,
					"imsbr_(process_packet|packet_relay2cp): (\d+) callbacks suppressed")
			if not match:
				return False
			if match.group(1) == "process_packet":
				self.pkts_fromcp += int(match.group(2))
			else:
				self.pkts_tocp += int(match.group(2))
				
		return True

	def dump_overview(self, lineno, time, ho):
		errmsg = None

		if ho == "ho-wifi2lte" and self.vowifi_tuples < 2:
			errmsg = "VOWIFI TUPLES %d ADDED, BUT HANDOVER TO VOLTE!" %(self.vowifi_tuples)
		elif ho == "ho-lte2wifi" and self.volte_tuples < 2:
			errmsg = "VOLTE TUPLES %d ADDED, BUT HANDOVER TO VOWIFI!" %(self.volte_tuples)
		elif ho == "ho-finish":
			# Dump overview stats
			msg = "Handover overview: fromcp=%d, tocp=%d, sipcfails=%d, outputfails=%d" \
				%(self.pkts_fromcp, self.pkts_tocp, self.sipc_fails, self.output_fails)
			self.add_result(compose_dict(time, lineno, msg))

			if self.pkts_fromcp == 0:
				errmsg = "NO PACKETS FROM CP, NEED CP CHECK IT FIRST!"
			elif self.pkts_tocp == 0:
				if self.last_ho == "ho-lte2wifi":
					# No pakcets from wifi, and there are many packets from cp output failed.
					if self.pkts_fromcp > 0 and self.output_fails/self.pkts_fromcp > 0.7:
						errmsg = "IP ROUTE FAIL, SECURITY CHECK IT FIRST!"
					else:
						errmsg = "NO PACKETS RECV FROM WIFI!"
				elif self.last_ho == "ho-wifi2lte":
					errmsg = "NO PACKETS FROM USERSPACE, NEED CHECK VIRTUAL ROUTE!"

		if errmsg:
			self.add_result(compose_dict(time, lineno, errmsg, logging.ERROR))

	def parse_handover(self, lineno, time, line):
		'''
		Format:
		c0 imsbr: trigger handover [ho-lte2wifi]
		'''
		match = self.search_pattern("handover", line, "imsbr: trigger handover \[(.*)\]")
		if not match:
			return False

		ho = match.group(1)
		self.add_result(compose_dict(time, lineno, "Trigger " + ho))
		self.dump_overview(lineno, time, ho)

		self.last_ho = ho
		self.clear_stat()
		return True

def parse_imsbr(logname):
	try:
		f = open(logname, "r")
	except IOError, e:
		print "Open fail:", e
		return None

	p = imsbr_parser()
	last_lineno = 0
	last_time = ""

	for _lineno, line in enumerate(f):
		if " imsbr" not in line:
			continue

		#Format: 01-01 08:04:05.743 ...
		t = line.split()
		t = t[0] + " " + t[1]

		lineno = _lineno + 1
		last_lineno = lineno
		last_time = t

		if p.parse_tuple(lineno, t, line):
			continue
		if p.parse_calls(lineno, t, line):
			continue
		if p.parse_sipcfail(lineno, t, line):
			continue
		if p.parse_outfail(lineno, t, line):
			continue
		if p.parse_packet(lineno, t, line):
			continue
		if p.parse_handover(lineno, t, line):
			continue

	# Handover log maybe incomplete, in such situation, also
	# dump the overview
	if p.last_ho != "ho-finish":
		p.dump_overview(last_lineno, last_time, "ho-finish")

	f.close()
	return p.results

def main():
	if len(sys.argv) != 2:
		print "Usage:", sys.argv[0], "kernel.log"
		sys.exit(1)

	results = parse_imsbr(sys.argv[1])
	if not results:
		return

	for d in results:
		print "line%d: %s %s " %(d["lineno"], d["timestamp"], d["msg"])

if __name__ == '__main__':
	main()
