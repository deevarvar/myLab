# -*- coding=utf-8 -*-
# author: zhihua.ye@spreadtrum.com
# analyzed result may be changed due to different ui result
# in the main.pdf or in the report
class langBuilder():
    def __init__(self, zh='', en=''):
        self.phrase = dict()
        self.phrase['lang'] = dict()
        self.phrase['lang']['zh'] = zh
        self.phrase['lang']['en'] = en

    def geten(self):
        return self.phrase['lang']['en']

    def getzh(self):
        return self.phrase['lang']['zh']

def map2phrase(key, phrasemap):
    if type(phrasemap) is not dict:
        return key
    if key in phrasemap:
        return phrasemap[key].geten()
    else:
        return key

#S2B phrase
Reports2bphrase = dict()
Reports2bphrase['successed'] = dict()
Reports2bphrase['successed'] = langBuilder(zh="epdg驻网成功", en="epdg attach successfully")

Reports2bphrase['failed'] = dict()
Reports2bphrase['failed'] = langBuilder(zh="epdg驻网失败", en="epdg attach failed")

Reports2bphrase['stopped'] = dict()
Reports2bphrase['stopped'] = langBuilder(zh="epdg驻网停止", en="epdg attach stopped")

#Register callback
Reportregphrase = dict()
Reportregphrase['login_ok'] = dict()
Reportregphrase['login_ok'] = langBuilder(zh="VoWiFi注册成功", en="VoWiFi Registered")

Reportregphrase['login_failed'] = dict()
Reportregphrase['login_failed'] = langBuilder(zh="VoWiFi注册失败", en="VoWiFi Failed to Register")

Reportregphrase['logouted'] = dict()
Reportregphrase['logouted'] = langBuilder(zh="VoWiFi去注册", en="VoWiFi UnRegistered")

Reportregphrase['refresh_ok'] = dict()
Reportregphrase['refresh_ok'] = langBuilder(zh="VoWiFi 刷新注册成功", en="VoWiFi Re-Registered")

Reportregphrase['refresh_failed'] = dict()
Reportregphrase['refresh_failed'] = langBuilder(zh="VoWiFi 刷新注册失败", en="VoWiFi Failed to Re-Registered")

