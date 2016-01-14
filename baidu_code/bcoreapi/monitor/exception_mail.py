#-*- coding=utf-8 -*-
import smtplib
import os
import redis
from email.mime.text import MIMEText  
from settings import REDIS_CONF,PARTNERS,EXCEPTION_SEQ_FILES,MAIL_LIST,MAIL_HOST,MAIL_USER,MAIL_PASS,MAIL_POSTFIX,MAX_CINEMA_ID

r = redis.Redis(REDIS_CONF['HOST'],REDIS_CONF['PORT'],REDIS_CONF['DB'])

# 发送邮件
mailto_list=[(user+'@baidu.com') for user in MAIL_LIST] 
mail_host=MAIL_HOST
mail_user=MAIL_USER
mail_pass=MAIL_PASS
mail_postfix=MAIL_POSTFIX
## 邮件内容
content = ""
content += "<html><head><h1>异常场次报警</h1></head><body>"
## 旧版邮件：按照合作方和错误类型发送
'''
for error in REDIS_CONF['SEQ_XPT_Q']:
    xpt_q = REDIS_CONF['SEQ_XPT_Q'][error][0]
    content += "<h3>%s</h3>" % REDIS_CONF['SEQ_XPT_Q'][error][1]
    content += "<table border=1><tr><th>影院名称</th><th>合作方</th><th>发现时间</th><th>选座url</th></tr>"
    for current_partner in PARTNERS:
        while r.llen(xpt_q+'_'+current_partner) != 0 :
            xpt_data = r.rpop(xpt_q+'_'+current_partner).split(' ')
            cinema_name = xpt_data[0][2:-1].decode('unicode_escape').encode('UTF-8')
            third_from = xpt_data[1]
            seq_url = xpt_data[2]
            time_found = xpt_data[3]
            content += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (cinema_name,third_from,time_found,seq_url)
    content += "</table>"
content += "</body></html>"
'''
## 新版邮件：按照影院发送
cinema_seq_q = REDIS_CONF['CINEMA_SEQ_Q']
print cinema_seq_q
for current_cinema_id in range(int(MAX_CINEMA_ID)+1):
    cinema_id = str(current_cinema_id)
    cinema_xpt_q = REDIS_CONF['CINEMA_XPT_Q']+"_"+cinema_id
    if r.llen(cinema_xpt_q) == 0:
        continue
    print cinema_xpt_q
    # 获取影院失败场次比
    t_seq_no = 0
    f_seq_no = 0
    while r.llen(cinema_seq_q+'_'+cinema_id) != 0 :
        seq_status = r.rpop(cinema_seq_q+'_'+cinema_id).split(' ')[0]
        print 'seq_status:' + str(seq_status)
        if str(seq_status) == '0':
            t_seq_no += 1
        else:
            f_seq_no += 1
    print t_seq_no
    print f_seq_no
    error_rate = '%.2f' % (float(f_seq_no*100)/float(f_seq_no+t_seq_no)) + '%'
    print error_rate
    xpt_data = r.rpop(cinema_xpt_q).split(' ')
    cinema_name = xpt_data[0][2:-1].decode('unicode_escape').encode('UTF-8')         
    content += "<h4>影院名称：%s</h4>" % cinema_name
    content += "<h4>错误场次占比：%s</h4>" % error_rate
    content += "<table border=1><tr><th>发现时间</th><th>合作方</th><th>选座url</th></tr>"
    
    #while r.llen(cinema_xpt_q) != 0 :
    while True:
        third_from = xpt_data[1]
        seq_url = xpt_data[2]
        time_found = xpt_data[3]
        content += "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (time_found,third_from,seq_url)
        if r.llen(cinema_xpt_q) == 0 :
            break
        xpt_data = r.rpop(cinema_xpt_q).split(' ')
    content += "</table>"
content += "</body></html>"

print content


me="Movie online api moniter"+"<"+mail_user+"@"+mail_postfix+">"
msg = MIMEText(content,_subtype='html',_charset='utf-8')  
msg['Subject'] = "*******线上场次购票流程功能监控：试运行*******"
msg['From'] = me
msg['To'] = ";".join(mailto_list)  
#try:  
server = smtplib.SMTP()  
server.connect(mail_host)
server.login(mail_user,mail_pass)  
server.sendmail(me, mailto_list, msg.as_string())
server.close()
