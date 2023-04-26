import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailUtil(object):

    def send_email(self):
        # 定义SMTP服务器
        smtpsrever = 'smtp.qq.com'
        # 发送邮件的用户名和密码
        username = '3537519644@qq.com'
        password = 'yrcbtdgvymtsdaeh'  # 授权密码
        # 接收邮件的邮箱
        receiver = '2149730257@qq.com'

        # 创建邮件对象
        message = MIMEMultipart('relate')  # 这是固定写法，生成一个带附件的邮件对象; 邮件信息，内容为空 #相当于信封##related表示使用内嵌资源的形式，将邮件发送给对方
        subject = "测试报告"  # 邮件的主题

        # 邮件正文内容
        body_content = "你好，这是一个测试邮件！"

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


if __name__ == '__main__':
    EmailUtil().send_email()

