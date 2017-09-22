#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com
#TODO: use sqlite to convert .ini file into db

#sample bug:749083 , 749671, 751978


from event import *

mname = "Media Engine"
mediaevent = Event()

#1. call start, recv, send_recv, inactive, end time
mediaevent.addevent(key="(_VTSP_CMD_STREAM_VIDEO_START)", module=mname, groupnum=1, eventHandler=VideoStart)
mediaevent.addevent(key="(VTSP_STREAM_DIR_INACTIVE)", module=mname, groupnum=1)
mediaevent.addevent(key="(VTSP_STREAM_DIR_RECVONLY)", module=mname, groupnum=1)
mediaevent.addevent(key="(VTSP_STREAM_DIR_SENDONY)", module=mname, groupnum=1)
mediaevent.addevent(key="(VTSP_STREAM_DIR_SENDRECV)", module=mname, groupnum=1)
mediaevent.addevent(key="(_VTSP_CMD_STREAM_VIDEO_END)", module=mname, groupnum=1, eventHandler=VideoStop)

#2. camera setting id, resolution and fps
#CAMERA_ID = 'CaptureAttach'
#CaptureAttach stream [1] attach Camera 1, Facing front, Orientation 270
mediaevent.addevent(key="CaptureAttach stream \[(\d+)\] attach Camera (\d+), Facing (.*), Orientation (\d+)", module=mname, groupnum=4, eventHandler=AttachCam)
#CAMERA_SETTING_FPS = 'setCameraFPS'
#setCameraFPS, fps range 30000 -> 30000
mediaevent.addevent(key="setCameraFPS, .*fps range (\d+) -> (\d+)", module=mname, groupnum=2, eventHandler=CamFps)
#CAMERA_SETTING_RESOLUTION = 'sensor-rot'
mediaevent.addevent(key="set sensor-rot (\d+)\*(\d+)", module=mname, groupnum=2, eventHandler=VtResolution)

#3. codec setting type(h264?h265)) payload, bitrate, fps, width, height and cvo
#CODEC_SETTING = 'SetCdc'
#SetCdc stream [1] codec H264 pl 114 br 600000 fr 30 X 480 Y 640.
mediaevent.addevent(key="SetCdc stream \[(\d+)\] codec (.*) pl (\d+) br (\d+) fr (\d+) X (\d+) Y (\d+).", module=mname, groupnum=7,eventHandler=SetCodec)
#CVO_INFO = 'urn:3gpp:video-orientation'
mediaevent.addevent(key="CreateVideoSendStream:.*\[{name: urn:3gpp:video-orientation,, id: (\d+)}\]", module=mname, groupnum=1, eventHandler=SetCvo)
mediaevent.addevent(key="CreateVideoReceiveStream:.*\[{name: urn:3gpp:video-orientation,, id: (\d+)}\]", module=mname, groupnum=1)

#//4. modem configured AS value
#CALL_NETWORKBANDWIDTH = 'localVideoAsBwKbps'
#localVideoAsBwKbps 960 Kbps
mediaevent.addevent(key="localVideoAsBwKbps (\d+) Kbps", module=mname, groupnum=1, eventHandler=VideoAs)
#//5. camera real output fps、encode fps，bitrate
#REAL_OUTPOUT = 'send_statistics_proxy'
#WATERMELON: (send_statistics_proxy.cc:93): send stats input fps: 0, encode fps: 1, encode bps: 10526; ssrc 2775897723 :rtcp: total lost 0, loss ratio 0, jitter 0, max seq 0; rtp: sent packets 9, fec 0, nack 0; width 240 height 320

mediaevent.addevent(key="send_statistics_proxy.*input fps: (\d+).*encode fps: (\d+).*encode bps: (\d+);", module=mname, groupnum=3, eventHandler=SendStat)
#//6. received fps, bitrate, loss rate, jitter, rtt
#RECV_STATICTIS = 'receive_statistics_proxy'
#receive_statistics_proxy.cc:60): recv stats incoming fps 7 decode fps 17 render fps 17 packets 117 bitrate 419610 rtcp: total loss 0 loss ratio 0 jitter 644 max seq 79
mediaevent.addevent(key="receive_statistics_proxy.*incoming fps (\d+).*bitrate (\d+).*loss ratio (\d+).*jitter (\d+) max seq (\d+)", module=mname, groupnum=5, eventHandler=RecvStat)

#get rtt value... , why not combine these into one log..., Orz
#08-31 16:18:24.911  4117  4310 I MME     : 16:18:24.911 MVD: INFO: StatFillRtpRtcp Video RTCP RR stream [1], iJitter 7, irtt 75, iLoss 0.
mediaevent.addevent(key="MVD: INFO: StatFillRtpRtcp Video RTCP RR stream.*iJitter (\d+), irtt (\d+), iLoss (\d+)", module=mname, groupnum=3, eventHandler=VideoRtt)

#//7. first sps, pps and i frame decoded time
#FIRST_KEY_FRAME_TIME = 'get length' && 'complete 1' &&'type 0'
#WATERMELON: WebrtcOMXH264VideoDecoder:0x7608a701d660, get length 3474, complete 1, type 0, ts 28609819
mediaevent.addevent(key="WATERMELON.*get length.*type (\d),", module=mname, groupnum=1)


