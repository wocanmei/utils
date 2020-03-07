# coding:utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


class SendEmail(object):
    """
    smtp邮件功能封装
    """

    def __init__(self, host: str='', user: str='', password: str='', port: int=25,sender:str=None,receiver:list=None):
        """
        :param host: 邮箱服务器地址
        :param user: 登陆用户名
        :param password: 登陆密码
        :param port: 邮箱服务端口
        :param sender: 邮件发送者
        :param receive: 邮件接收者
        """
        self.HOST = host
        self.USER = user
        self.PASSWORD = password
        self.PORT = port
        if(sender!=None):
            self.SENDER = None
        if(receiver!=None):
            self.RECEIVE = None

        # 与邮箱服务器的连接
        self._server = smtplib.SMTP(self.HOST, self.PORT, timeout=2)
        self._server.login(self.USER, self.PASSWORD)
        # 邮件对象,用于构造邮件内容
        self._email = None


    def add_email_header(self,subject='python email',fromm:str=None,to:list=None):
        """构造邮件对象
        subject: 邮件主题
        from: 邮件发送方
        to: 邮件接收方
        """
        if(fromm!=None):
            self.SENDER=fromm
        if(to!=None):
            self.RECEIVE=to   
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = self.SENDER
        msg['To'] = ';'.join(self.RECEIVE)
        self._email = msg

    def add_content(self, content: str, _type: str = 'txt'):
        """给邮件对象添加正文内容"""
        if _type == 'txt':
            text = MIMEText(content, 'plain', 'utf-8')
        if _type == 'html':
            text = MIMEText(content, 'html', 'utf-8')

        self._email.attach(text)

    def add_file(self, file_path: str):
        """
        给邮件对象添加附件
        :param file_path: 文件路径
        :return: None
        """
        # 构造附件1，传送当前目录下的 test.txt 文件
        email_file = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
        email_file["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        file_name = os.path.basename(file_path)
        # 下面这种写法，如果附件名是中文，会出现乱码问题，修改成如下写法
        # email_file["Content-Disposition"] = f'attachment; filename="{file_name}"'
        email_file.add_header("Content-Disposition", "attachment", filename=file_name)
        self._email.attach(email_file)

    def send_email(self):
        """发送邮件"""
        # 使用send_message方法而不是sendmail,避免编码问题
        print(self._email)
        self._server.send_message(from_addr=self.SENDER, to_addrs=self.RECEIVE, msg=self._email)

    def quit(self):
        self._server.quit()

    def close(self):
        self._server.close()


if __name__ == '__main__':
    email = SendEmail('smtp.sina.com','**@sina.com','16passwd',25)
    email.add_email_header(subject='python mail test',fromm='**@sina.com',to=['**@sina.com'])
    email.add_content(content='hello world')
    email.send_email()
    email.close()