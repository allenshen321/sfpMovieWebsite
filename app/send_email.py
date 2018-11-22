# 定义发送邮件

from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header
from flask import current_app


def send_text_email(mail_from=None, mail_to=None, mail_to_name=None, msg=None):
    """
    发送邮件
    :param send_from: 发送者的邮箱，配置文件的FLASK_EMAIL_FROM
    :param send_to: 接受者的邮箱地址
    :param msg: 发送邮件的信息
    :return: None
    """
    if not mail_from:
        mail_from = current_app.config['FLASK_MAIL_NAME']
    mail_password = current_app.config['FLASK_MAIL_PASSWORD']
    smtp_server = current_app.config['FLASK_MAIL_SERVER']
    smtp_port = current_app.config['FLASK_MAIL_PORT']
    # 发送邮箱信息
    mail_msg = msg

    # 构造邮件信息
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header('随风飘电影', 'utf-8')
    message['To'] = Header(mail_to_name, 'utf-8')

    subject = '随风飘电影网站用户确认邮件'
    message['Subject'] = Header(subject, 'utf-8')

    # 发送邮件
    server = SMTP(smtp_server, smtp_port)
    server.set_debuglevel(1)
    server.login(mail_from, mail_password)
    server.sendmail(mail_from, mail_to, mail_msg.as_string())

