#-*- coding=utf-8 -*-
#author: zhihua.ye@spreadtrum.com

Q850map = dict()

Q850map['1'] = dict()
Q850map['1']['isdn'] = "unallocated number"
Q850map['1']['sip'] = "404 Not found"

Q850map['2'] = dict()
Q850map['2']['isdn'] = "no route to network"
Q850map['2']['sip'] = "404 Not found"

Q850map['3'] = dict()
Q850map['3']['isdn'] = "no route to destination"
Q850map['3']['sip'] = "404 Not found"

Q850map['6'] = dict()
Q850map['6']['isdn'] = "CHANNEL_UNACCEPTABLE"
Q850map['6']['sip'] = ""

Q850map['7'] = dict()
Q850map['7']['isdn'] = "CALL_AWARDED_DELIVERED"
Q850map['7']['sip'] = ""

Q850map['16'] = dict()
Q850map['16']['isdn'] = "NORMAL_CLEARING"
Q850map['16']['sip'] = ""

Q850map['17'] = dict()
Q850map['17']['isdn'] = "17 user busy"
Q850map['17']['sip'] = "486 Busy here"

Q850map['18'] = dict()
Q850map['18']['isdn'] = "no user responding"
Q850map['18']['sip'] = "408 Request Timeout"

Q850map['19'] = dict()
Q850map['19']['isdn'] = "no answer from the user"
Q850map['19']['sip'] = "480 Temporarily unavailable"

Q850map['20'] = dict()
Q850map['20']['isdn'] = "subscriber absent"
Q850map['20']['sip'] = "480 Temporarily unavailable"

Q850map['21'] = dict()
Q850map['21']['isdn'] = "call rejected"
Q850map['21']['sip'] = "603 Decline"


Q850map['22'] = dict()
Q850map['22']['isdn'] = "number changed"
Q850map['22']['sip'] = "410 Gone"

Q850map['23'] = dict()
Q850map['23']['isdn'] = "redirection to new destination"
Q850map['23']['sip'] = "410 Gone"


Q850map['25'] = dict()
Q850map['25']['isdn'] = "EXCHANGE_ROUTING_ERRORn"
Q850map['25']['sip'] = "483 Too Many Hops"

Q850map['26'] = dict()
Q850map['26']['isdn'] = "non-selected user clearing"
Q850map['26']['sip'] = "404 Not Found"

Q850map['27'] = dict()
Q850map['27']['isdn'] = "destination out of order"
Q850map['27']['sip'] = "502 Bad Gateway"

Q850map['28'] = dict()
Q850map['28']['isdn'] = "address incomplete"
Q850map['28']['sip'] = "484 Address incomplete"

Q850map['29'] = dict()
Q850map['29']['isdn'] = "facility rejected"
Q850map['29']['sip'] = "501 Not implemented"

Q850map['30'] = dict()
Q850map['30']['isdn'] = "RESPONSE_TO_STATUS_ENQUIRY"
Q850map['30']['sip'] = ""

Q850map['31'] = dict()
Q850map['31']['isdn'] = "normal unspecified"
Q850map['31']['sip'] = "480 Temporarily unavailable"

Q850map['34'] = dict()
Q850map['34']['isdn'] = "no circuit available"
Q850map['34']['sip'] = "503 Service unavailable"

Q850map['38'] = dict()
Q850map['38']['isdn'] = "network out of order"
Q850map['38']['sip'] = "503 Service unavailable"

Q850map['41'] = dict()
Q850map['41']['isdn'] = "temporary failure"
Q850map['41']['sip'] = "503 Service unavailable"

Q850map['42'] = dict()
Q850map['42']['isdn'] = "switching equipment congestion"
Q850map['42']['sip'] = "503 Service unavailable"

Q850map['43'] = dict()
Q850map['43']['isdn'] = "ACCESS_INFO_DISCARDED"
Q850map['43']['sip'] = ""

Q850map['44'] = dict()
Q850map['44']['isdn'] = "REQUESTED_CHAN_UNAVAIL"
Q850map['44']['sip'] = "503 Service unavailable"

Q850map['45'] = dict()
Q850map['45']['isdn'] = "PRE_EMPTED"
Q850map['45']['sip'] = ""

Q850map['47'] = dict()
Q850map['47']['isdn'] = "resource unavailable"
Q850map['47']['sip'] = "503 Service unavailable"

Q850map['50'] = dict()
Q850map['50']['isdn'] = "FACILITY_NOT_SUBSCRIBED"
Q850map['50']['sip'] = ""

Q850map['52'] = dict()
Q850map['52']['isdn'] = "OUTGOING_CALL_BARRED"
Q850map['52']['sip'] = "403 Forbidden"


Q850map['54'] = dict()
Q850map['54']['isdn'] = "incoming calls barred"
Q850map['54']['sip'] = "403 Forbidden"

Q850map['57'] = dict()
Q850map['57']['isdn'] = "bearer capability not authorized"
Q850map['57']['sip'] = "403 Forbidden"

Q850map['58'] = dict()
Q850map['58']['isdn'] = "BEARERCAPABILITY_NOTAVAIL"
Q850map['58']['sip'] = "503 Service unavailable"

Q850map['65'] = dict()
Q850map['65']['isdn'] = "BEARERCAPABILITY_NOTIMPL"
Q850map['65']['sip'] = "488 Not Acceptable Here"

Q850map['66'] = dict()
Q850map['66']['isdn'] = "CHAN_NOT_IMPLEMENTED"
Q850map['66']['sip'] = ""

Q850map['69'] = dict()
Q850map['69']['isdn'] = "FACILITY_NOT_IMPLEMENTED"
Q850map['69']['sip'] = "501 Not implemented"

Q850map['70'] = dict()
Q850map['70']['isdn'] = "only restricted digital available"
Q850map['70']['sip'] = "488 Not Acceptable Here"

Q850map['79'] = dict()
Q850map['79']['isdn'] = "SERVICE_NOT_IMPLEMENTED"
Q850map['79']['sip'] = "501 Not implemented"


Q850map['81'] = dict()
Q850map['81']['isdn'] = "INVALID_CALL_REFERENCE"
Q850map['81']['sip'] = ""

Q850map['87'] = dict()
Q850map['87']['isdn'] = "user not member of CUG"
Q850map['87']['sip'] = "403 Forbidden"

Q850map['88'] = dict()
Q850map['88']['isdn'] = "incompatible destination"
Q850map['88']['sip'] = "503 Service unavailable"

Q850map['95'] = dict()
Q850map['95']['isdn'] = "INVALID_MSG_UNSPECIFIED"
Q850map['95']['sip'] = ""

Q850map['96'] = dict()
Q850map['96']['isdn'] = "MANDATORY_IE_MISSING"
Q850map['96']['sip'] = ""

Q850map['97'] = dict()
Q850map['97']['isdn'] = "MESSAGE_TYPE_NONEXIST"
Q850map['97']['sip'] = ""

Q850map['98'] = dict()
Q850map['98']['isdn'] = "WRONG_MESSAGE"
Q850map['98']['sip'] = ""

Q850map['100'] = dict()
Q850map['100']['isdn'] = "INVALID_IE_CONTENTS"
Q850map['100']['sip'] = ""

Q850map['101'] = dict()
Q850map['101']['isdn'] = "WRONG_CALL_STATE"
Q850map['101']['sip'] = ""

Q850map['103'] = dict()
Q850map['103']['isdn'] = "MANDATORY_IE_LENGTH_ERROR"
Q850map['103']['sip'] = ""

Q850map['102'] = dict()
Q850map['102']['isdn'] = "recovery of timer expiry"
Q850map['102']['sip'] = "504 Gateway timeout"

Q850map['111'] = dict()
Q850map['111']['isdn'] = "protocol error"
Q850map['111']['sip'] = "500 Server internal error"


Q850map['127'] = dict()
Q850map['127']['isdn'] = "inter-working unspecified"
Q850map['127']['sip'] = "500 Server internal error"


Q850map['487'] = dict()
Q850map['487']['isdn'] = "ORIGINATOR_CANCEL"
Q850map['487']['sip'] = "487 Request Terminated"

Q850map['500'] = dict()
Q850map['500']['isdn'] = "CRASH"
Q850map['500']['sip'] = ""

Q850map['501'] = dict()
Q850map['501']['isdn'] = "SYSTEM_SHUTDOWN"
Q850map['501']['sip'] = ""

Q850map['502'] = dict()
Q850map['502']['isdn'] = "LOSE_RACE"
Q850map['502']['sip'] = ""

Q850map['503'] = dict()
Q850map['503']['isdn'] = "MANAGER_REQUEST"
Q850map['503']['sip'] = ""

Q850map['600'] = dict()
Q850map['600']['isdn'] = "BLIND_TRANSFER"
Q850map['600']['sip'] = ""

Q850map['601'] = dict()
Q850map['601']['isdn'] = "ATTENDED_TRANSFER"
Q850map['601']['sip'] = ""


Q850map['602'] = dict()
Q850map['602']['isdn'] = "ALLOTTED_TIMEOUT"
Q850map['602']['sip'] = ""


Q850map['603'] = dict()
Q850map['603']['isdn'] = "USER_CHALLENGE"
Q850map['603']['sip'] = ""

Q850map['604'] = dict()
Q850map['604']['isdn'] = "MEDIA_TIMEOUT"
Q850map['604']['sip'] = ""

Q850map['605'] = dict()
Q850map['605']['isdn'] = "PICKED_OFF"
Q850map['605']['sip'] = ""


Q850map['606'] = dict()
Q850map['606']['isdn'] = "USER_NOT_REGISTERED"
Q850map['606']['sip'] = ""


Q850map['607'] = dict()
Q850map['607']['isdn'] = "PROGRESS_TIMEOUT"
Q850map['607']['sip'] = ""

Q850map['609'] = dict()
Q850map['609']['isdn'] = "GATEWAY_DOWN"
Q850map['609']['sip'] = ""