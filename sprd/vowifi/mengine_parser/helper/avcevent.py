#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

from event import *

avcname="SPRDAVC"
avcevent = Event()
#nal_type:7,sps, nal_type:8, pps
# SPRDAVCDecoder: findCodecConfigData, queueSize:1, bufferHeader:0xb402e360, nal_type:7, nal_ref_idc:3
avcevent.addevent(key="SPRDAVCDecoder.*nal_type:(\d)", module=avcname, groupnum=1)

avcevent.addevent(key="SPRDAVCDecoder.*decRet:(.*),.*dec_out.frameEffective:(.*), needIVOP: (\d),", module=avcname, groupnum=3)
avcevent.addevent(key="SPRDAVCEncoder.*H264EncStrmEncode\[(.*)\] (\d+)ms", module=avcname, groupnum=2)
