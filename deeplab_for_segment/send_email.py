# -*- coding: utf-8 -*-
# @Time    : 4/28/2018 10:07 AM
# @Author  : sunyonghai
# @File    : send_email.py
# @Software: ZJ_AI

import smtplib
from email.mime.text import MIMEText
import time

def notify(content):
<<<<<<< HEAD
    msg_from = '1640968638@qq.com'  # 发送方邮箱
    passwd = 'rngdvajabbndbbcj'  # 填入发送方邮箱的授权码
    # msg_to = '931103972@qq.com, 841861601@qq.com,2092089369@qq.com'  # 收件人邮箱
    msg_to = ['1640968638@qq.com']#['Firmin.Sun@outlook.com','jiangxiaobaix@outlook.com', ] # 收件人邮箱
=======
    msg_from = 'choubin@outlook.com'  # 发送方邮箱
    passwd = 'nrpsrzgwsmssbahf'  # 填入发送方邮箱的授权码
    # msg_to = '931103972@qq.com, 841861601@qq.com,2092089369@qq.com'  # 收件人邮箱
    msg_to = ['Firmin.Sun@outlook.com','jiangxiaobaix@outlook.com', 'jaykky.Lu@outlook.com'] # 收件人邮箱
>>>>>>> a9edff3cf27d4816c1c4159c5b10b70e16eed107

    subject = "segmentation result sent to tfp server"  # 主题
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    # msg['To'] = msg_to
<<<<<<< HEAD
    
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.connect("smtp.qq.com")
=======
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
>>>>>>> a9edff3cf27d4816c1c4159c5b10b70e16eed107
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print('Send email successful')
    except Exception as ex :
        print( 'Failed:'.format(ex))
    finally:
        s.quit()

if __name__ == '__main__':
    #取得当前时间戳
    print(time.time())
    #格式化时间戳为标准格式
    print (time.strftime('%Y.%m.%d',time.localtime(time.time())))
    content = 'hello, send by Python...'
    notify(content)