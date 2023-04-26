import re
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from lxml import etree


def send_email(weibo_text):
    # 定义SMTP服务器
    smtpsrever = 'smtp.qq.com'
    # 发送邮件的用户名和密码
    username = '3537519644@qq.com'
    password = 'yrcbtdgvymtsdaeh'  # 授权密码
    # 接收邮件的邮箱
    receiver = '2149730257@qq.com'

    # 创建邮件对象
    message = MIMEMultipart('relate')  # 这是固定写法，生成一个带附件的邮件对象; 邮件信息，内容为空 #相当于信封##related表示使用内嵌资源的形式，将邮件发送给对方
    subject = "有新的微博"  # 邮件的主题

    # 邮件正文内容
    body_content = weibo_text

    message_text = MIMEText(body_content, "plain", "utf-8")

    # 把邮件的信息组装到邮件对象里
    message['from'] = username
    message['to'] = receiver
    message['subject'] = subject
    message.attach(message_text)

    # 登录smtp服务器并发送邮件
    smtp = smtplib.SMTP()
    smtp.connect(smtpsrever)
    smtp.login(username, password)
    smtp.sendmail(username, receiver, message.as_string())
    smtp.quit()


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
}
url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=6616783528&containerid=1076036616783528'
# url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=6507748358&containerid=1076036507748358'

old_text = ' '
while True:
    page_text = requests.get(url=url, headers=header).text
    p = re.compile(r'"text":".*?",')
    q = re.compile(r'\\u....')
    # print(page_text)
    res = p.findall(page_text)
    res_2 = q.findall(res[0])
    # print(len(res))

    # print(res[0])
    # print(res_2)

    text = ''
    for word in res_2:
        # print(word)
        text += word.encode('utf-8').decode('unicode-escape')
    # print(text)
    if text != old_text:
        # print(text)
        old_text = text
        with open('weibo.txt', 'a') as f:
            f.write(str(time.asctime()) + ' ' + text + '\n')
        send_email(text)

    time.sleep(30)
