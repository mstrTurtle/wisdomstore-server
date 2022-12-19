import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import json
'''
使用Python及SMTP协议发送邮件（以163邮箱为例）
一是尝试封装成类，和支持with上下文管理器。
二是构建了text和mutli两种类型的邮件。
三是实现抄送和独立出附件添加。
'''

emconfig={}



class EmailLogger:
    logpath = None

    @classmethod
    def log(cls, text):
        if not cls.logpath:
            cls.logpath = 'email.log'
            print('LogPath Error. Auto output to "email.log"')
        with open(cls.logPath, 'ab+') as f:
            f.write(f'{text}\n'.encode(encoding='utf8'))

try:
    with open('em_config.json') as f:
        s = f.read()
    emconfig = json.loads(s)
    EmailLogger.logpath = emconfig['logPath']
except Exception as e:
    EmailLogger.log('Exception raised when loading config: ' + repr(e))
        
 
class My163:
    def __init__(self):
        self._mail_host = emconfig['host']  # 163邮箱服务器地址
        self._mail_user = emconfig['user'] # 163用户名
        self._mail_pass = emconfig['passwd']  # 密码(部分邮箱为授权码)
        # self._smtpObj = smtplib.SMTP()  # 根据是否ssl认证进行二选一
        self._smtpObj = smtplib.SMTP_SSL(self._mail_host, port=465)  # 根据是否ssl认证进行二选一
 
    def __enter__(self):
        EmailLogger.log('Info: Enter My163 ... ')
        try:
            # 连接到服务器
            # self._smtpObj.connect(host=self._mail_host, port=25)
            self._smtpObj.connect(host=self._mail_host, port=465)
            # 登录到服务器
            res = self._smtpObj.login(user=self._mail_user, password=self._mail_pass)
            EmailLogger.log(f'登录结果：{res}')
        except smtplib.SMTPException as e:
            EmailLogger.log("163 email login failed with error: %s" % e)  # 打印错误
        finally:
            return self  # 注意enter里面一定要返回类的对象self,否则无法调用run方法。
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        EmailLogger.log('Info: Exit My163')
        self._smtpObj.quit()
 
    def email_send(self, to_addrs, message):
        '''
        # 邮件发送
        :param to_addrs: 包含所有收件人的列表
        :param message: 邮件格式化的字符串，或邮件对象
        如 message = '\n'.join(['From: {}'.format(FROM), 'To: {}'.format(TO), 'Subject: {}'.format(SUBJECT), '', CONTENT])
        :return:
        '''
        try:
            rst = self._smtpObj.sendmail(from_addr=self._mail_user, to_addrs=to_addrs, msg=str(message))
            # EmailLogger.log(f'rst: {rst}')
            return True
        except Exception as e:
            EmailLogger.log("163 email login failed with error: %s" % e)  # 打印错误
            return False
 
    def textMail_send(self,
                      from_addr='Cameback_Tang',
                      to_addrs=['769711153@qq.com'],
                      cc_addrs=[],
                      bcc_addrs=[],
                      subject='传智商城通知',
                      content='messageText'):
        '''
            发送字符串等正文文本信息，使用 MIMEText 对象，不能附件
            :param from_addr: 其实只是别名，效果：XXXXX@163.com on behalf of xxxxxx@163.com
            :param to_addrs: 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
            :param cc_addrs: 抄送人列表
            :param bcc_addrs: 秘密抄送人列表
            :param title: 邮件标题
            :param content: 邮件内容
            :return:
        '''
        ## 1、邮件正文文本信息，可以使用 MIMEText 对象
        # 实例化简单邮件对象，邮件正文内容设置
        # 若_text参数传递了文本字符串，则_subtype参数应该传递’plain’。
        # 若_text参数传递了二进制文件，则_subtype参数应该传递’base64’。
        msg = MIMEText(content, 'plain', 'utf-8')
 
        # 2、设置设置邮件信息：邮件主题、发送人、收件人、抄送、秘密抄送
        # 我们使用三个引号来设置邮件信息，标准邮件需要三个头部信息： From, To, 和 Subject ，每个信息直接使用空行分割。
        # from email.header import Header
        # msg['Subject'] = Header('xmy的作业', 'utf-8').encode()
        msg['Subject'] = subject
        # msg['From'] = f'{from_addr}<{self._mail_user}>'
        msg['From'] = from_addr
        msg['To'] = ";".join(to_addrs)  # 重复设置属追加字段，不会替换。
        msg['Cc'] = ";".join(cc_addrs)
        msg['Bcc'] = ";".join(bcc_addrs)
 
        # 3、给 所有收件人 send email
        addressees = to_addrs + cc_addrs + bcc_addrs
        return self.email_send(to_addrs=addressees, message=msg)
 
    def add_image_attachment(self, multiMsg, filePath, filenameInEmail=None):
        '''
            添加照片附件
            :param multiMsg: MIMEMultipart()，实例化复合邮件对象
            :param filePath: 文件路径：需要检查 filePath 是否存在
            :param filenameInEmail: 邮件中的附件命名，默认None即使用filePath中的文件名字
            :return:
            '''
        if os.path.exists(filePath):
            pass
        else:
            EmailLogger.log(f'找不到附件：{filePath}')
            EmailLogger.log('请将附件上传到项目目录')
            return multiMsg
 
        if filenameInEmail:
            pass
        else:
            filenameInEmail = os.path.basename(filePath)
 
        with open(filePath, 'rb') as fp:
            picture = MIMEImage(fp.read())
            picture['Content-Type'] = 'application/octet-stream'  # 附件设置内容类型，方便起见，设置为二进制流
            picture['Content-Disposition'] = f'attachment; filename="{filenameInEmail}"'  # 附件命名
            multiMsg.attach(picture)
        return multiMsg
 
    def add_text_attachment(self, multiMsg, filePath, filenameInEmail=None):
        '''
            添加文本附件
            :param multiMsg: MIMEMultipart()，实例化复合邮件对象
            :param filePath: 文件路径：需要检查 filePath 是否存在 todo
            :param filenameInEmail: 邮件中的附件命名，默认None即使用filePath中的文件名字
            :return:
            '''
        if os.path.exists(filePath):
            pass
        else:
            EmailLogger.log(f'找不到附件：{filePath}')
            EmailLogger.log('请将附件上传到项目目录')
            return multiMsg
 
        if filenameInEmail:
            pass
        else:
            filenameInEmail = os.path.basename(filePath)
 
        # # 添加文件附件
        with open(filePath, 'rb') as f:
            # 以二进制读入文件，创建文本邮件对象
            file_data = MIMEText(f.read(), 'base64', 'utf-8')
            # file_data.add_header('Content-Disposition', 'attachment; filename="countryCode.xlsx"')
            file_data['Content-Type'] = 'application/octet-stream'  # 附件设置内容类型，方便起见，设置为二进制流
            file_data['Content-Disposition'] = f'attachment; filename="{filenameInEmail}"'  # 附件命名
            multiMsg.attach(file_data)  # 添加附件到复合邮件对象中, attach一次只能放一个简单邮件对象
        return multiMsg
 
    def multiTypeMailer_send(self,
                             from_addr='Cameback_Tang',
                             to_addrs=['111222333@qq.com'],
                             cc_addrs=[],
                             bcc_addrs=[],
                             subject='emailTitle',
                             mail_html_msg='<p>人生苦短，我用Python</p>',
                             attachments=None):
        '''
            发送带附件的邮件，首先要创建 MIMEMultipart()实例，然后构造附件，如果有多个附件，可依次构造，
            :param from_addr: 其实只是别名，效果：XXXXX@163.com on behalf of xxxxxx@163.com
            :param to_addrs: 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
            :param cc_addrs: 抄送人列表
            :param bcc_addrs: 秘密抄送人列表
            :param title: 邮件标题
            :param mail_html_msg: 邮件内容
            :param attachments: 附件路径列表
            :return:
            '''
        # 1、构造MIMEMultipart对象作为根容器
        # 实例化复合邮件对象。它可以用来装载多个简单邮件对象
        msg = MIMEMultipart()
 
        # # 3、邮件正文
        # 推荐使用html格式的正文内容，这样比较灵活，可以附加图片地址，调整格式等。    # 添加HTML内容, 三双引号
        # 可以使用 MIMEMultipart 对象，也可以使用 MIMEText 对象， 并添加正文到复合邮件对象中
        msgContent = MIMEMultipart()
        msg.attach(msgContent)
 
        msgContent.attach(MIMEText(mail_html_msg, 'html', 'utf-8'))
 
        # # 4、邮件附件，读取附件内容， 注意以“二进制读”方式读取
        # 文本、图片、音频
        if attachments:
            for attachment in attachments:
                basename = os.path.basename(attachment)
                attachment_type = basename.split('.')[1]  # 如'image1.png'為 image1
                if attachment_type in ['txt', 'csv', 'xlsx', 'py']:
                    msg = self.add_text_attachment(msg, filePath=attachment, filenameInEmail=None)
                elif attachment_type in ['png', 'jpg']:
                    msg = self.add_image_attachment(msg, filePath=attachment, filenameInEmail=None)
                else:
                    EmailLogger.log(f'附件添加失败，属代码不支持的未知文件类型：{attachment}')
 
        # 2、设置设置邮件信息
        # 邮件主题、发送人(可以别名)、收件人、抄送、秘密抄送
        # 5、给 所有收件人 send email
        msg['Subject'] = subject
        msg['From'] = f'{from_addr}<{self._mail_user}>'
        msg['to'] = ";".join(to_addrs)
        msg['Cc'] = ";".join(cc_addrs)
        msg['Bcc'] = ";".join(bcc_addrs)
        addressees = to_addrs + cc_addrs + bcc_addrs
        return self.email_send(message=msg, to_addrs=addressees)
 
 
def sendEmailSerivce(target_addr, msg):
    with My163() as my163:
        EmailLogger.log(f'sending to: "{target_addr}"')
        my163.textMail_send( from_addr='qq769711153@163.com',to_addrs=[target_addr], content=msg)
