import smtplib, os
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.message import MIMEMessage
from email.mime.base import MIMEBase
from email import encoders
from smtplib import SMTP, SMTP_SSL
from appconfig import AppConfig

class SMTPConnect():
    CODE_OK = 'ok'
    CODE_FAIL = 'fail'

    def __init__(self):
        self.__smtpOptions = AppConfig().sessionOptions()
        

    def connect(self, config):
        '''
        server is config name set on _smtpOptions
        return {
            'code':CODE_,
            'message:''
        }
        '''
        
        outputMessage = {
            'code':SMTPConnect.CODE_FAIL,
            'message':None
        }

        smtpConfig = self.__smtpOptions.get(config)
        if smtpConfig:
            ssl = smtpConfig.get('ssl')
            server = smtpConfig.get('server')
            port = smtpConfig.get('port')
            user = smtpConfig.get('user')
            password = smtpConfig.get('password')

            if ssl and ssl.get('certfile') and ssl.get('keyfile'):
                outputMessage = self.__connectSMTPSSL(server, port, user, password, certfile=ssl.get('certfile'), keyfile=ssl.get('keyfile'))

            else:
                outputMessage = self.__connectSMTP(server, port, user, password)

                if outputMessage.get('code') == SMTPConnect.CODE_FAIL:
                    outputMessage = self.__connectSMTPSSL(server, port, user, password)

        else:
            outputMessage['message'] = 'smtp configuration for {} not found'.format(config)

        return outputMessage


    def quit(self):

        outputMessage = {
            'code':SMTPConnect.CODE_OK,
            'message':'Quit smtp session'
        }

        if self.__smtp:
            try:
                self.__smtp.quit()

            except Exception as ex:
                outputMessage['message'] = 'Failed when quit the smptp session {}'.format(ex)

        return outputMessage


    def __connectSMTP(self, host, port, user, password):
        '''
        return
        {
            'code':CODE_,
            'message':''
        }
        '''

        outputMessage = {
            'code':SMTPConnect.CODE_FAIL,
            'message':None
        }

        try:
            self.__smtp = SMTP(host, port)
            self.__smtp.login(user, password)
            outputMessage['code'] = SMTPConnect.CODE_OK
            outputMessage['message'] = 'Success connected to {} {}'.format(host, port)

        except Exception as ex:
            outputMessage['message'] = 'Failed {}'.format(ex)

        return outputMessage

    
    def __connectSMTPSSL(self, host, port, user, password, certfile=None, keyfile=None):
        '''
        return
        {
            'code':CODE_,
            'message':''
        }
        '''

        outputMessage = {
            'code':SMTPConnect.CODE_FAIL,
            'message':None
        }

        try:
            self.__smtp = SMTP_SSL(host, port, certfile=certfile, keyfile=keyfile)
            self.__smtp.login(user, password)
            outputMessage['code'] = SMTPConnect.CODE_OK
            outputMessage['message'] = 'Success connected to {} {}'.format(host, port)

        except Exception as ex:
            outputMessage['message'] = 'Failed {}'.format(ex)

        return outputMessage


    def sendMessage(self, messageBuilder):
        '''
        message builder is from MessageBuilder class instance
        '''

        outputMessage = {
            'code':SMTPConnect.CODE_FAIL,
            'message':None
        }

        try:
            self.__smtp.send_message(messageBuilder.generate())
            outputMessage['code'] = SMTPConnect.CODE_OK
            outputMessage['message'] = 'Success sending message'

        except Exception as ex:
            outputMessage['message'] = 'Failed sending message {}'.format(ex)


        return outputMessage


class MessageBuilder():
    '''
        build email to make it easy to send
    '''

    COMMASPACE = ', '
    
    def __init__(self):
        '''
            msg_from = 'amru.rosyada@gmail.com'
            msg_to = ['john@gmail.com', 'doe@gmail.com']
            msg_subject = 'Good Morning'
        '''
        
        self.__message = MIMEMultipart()
        self.__messageAttachment = []
        self.__rcptOptions = []
        self.__mailOptions = []


    def sender(self, sender):
        self.__message['from'] = sender
        return self


    def sendTo(self, sendTo=[]):
        self.__message['To'] = MessageBuilder.COMMASPACE.join(sendTo)
        return self


    def subject(self, subject):
        self.__message['Subject'] = subject
        return self

        
    def ccTo(self, ccTo=[]):
        '''
            ccTo should be in list string of email address format
            ccTo = ['a@domain.com', 'b@domain.com']
        '''
        
        self.__message['CC'] = MessageBuilder.COMMASPACE.join(ccTo)
        return self

        
    def bccTo(self, bccTo=[]):
        '''
            bccTo should be in list string of email address format
            bccTo = ['a@domain.com', 'b@domain.com']
        '''
        
        self.__message['BCC'] = MessageBuilder.COMMASPACE.join(bccTo)
        return self

        
    def mailOptions(self, mailOptions=[]):
        '''
            add mail options
            options is like send_mail options
            see smtplib send_mail
            should be in list
        '''
        
        self.__mailOptions = mailOptions
        return self

        
    def rcptOptions(self, rcptOptions=[]):
        '''
            add recepient options
            options is like send_mail options
            see smtplib send_mail
        '''
        
        self.__rcptOptions = rcptOptions
        return self

            
    def attachApplication(self, filePath, mimeType='octet-stream', encoder=encoders.encode_base64, disposition=True, **param):
        '''
            attach application
            example:
                attachApplication('/home/amru/timesheet.xlsx')
        '''

        self.__messageAttachment.append({
                'file':filePath,
                'mimeType':mimeType,
                'encoder':encoder,
                'param':param,
                'disposition':disposition,
                'type':'application'
            })
            
        return self

        
    def attachText(self, text, mimeType='plain', charset=None, disposition=False):
        '''
            attach text can be as disposition or not
            default is not disposition
            if disposition True, text should be to filePath, like '/home/amru/test.txt'
        '''

        self.__messageAttachment.append({
                'file':text,
                'mimeType':mimeType,
                'charset':charset,
                'disposition':disposition,
                'type':'text'
            })
            
        return self


    def attachImage(self, filePath, mimeType=None, encoder=encoders.encode_base64, disposition=True, **params):
        '''
            attach image
            example:
                attachImage('/home/amru/timesheet.png')
        '''

        self.__messageAttachment.append({
                'file':filePath,
                'mimeType':mimeType,
                'encoder':encoder,
                'param':param,
                'disposition':disposition,
                'type':'image',
            })
            
        return self

        
    def attachMessage(self, messageObj, mimeType='rfc822', disposition=True):
        '''
            attach message
            example:
                attachMessage(messageObj)
        '''

        self.__messageAttachment.append({
                'msg':messageObj,
                'mimeType':mimeType,
                'disposition':disposition,
                'type':'message',
            })
            
        return self


    def attachAudio(self, filePath, mimeType=None, encoder=encoders.encode_base64, disposition=True, **param):
        '''
            attach audio
            example:
                attachAudio('/home/amru/timesheet.ogg')
        '''

        self.__messageAttachment.append({
                'file':filePath,
                'mimeType':mimeType,
                'encoder':encoder,
                'param':param,
                'disposition':disposition,
                'type':'audio'
            })
            
        return self


    def attachBase(self, filePath, mimeMain='application', mimeType='octet-stream', encoder=encoders.encode_base64, disposition=True, **param):
        '''
            attach base
            example:
                attachBase('/home/amru/timesheet.ogg', 'audio/ogg-vorbis')
        '''

        self.__messageAttachment.append({
                'file':filePath,
                'main_mime':mimeMain,
                'mimeType':mimeType,
                'encoder':encoder,
                'param':param,
                'disposition':disposition,
                'type':'base'
            })

        return self

        
    def generate(self):
        '''
            generate message to send with send message
        '''

        for attachment in self.__messageAttachment:
            part = None
            f = None
            
            if attachment.get('type') == 'application':
                f = open(attachment.get('file'), 'rb')
                part = MIMEApplication(
                    f.read(),
                    attachment.get('mimeType'),
                    attachment.get('encoder'),
                    **attachment.get('param'))
                    
            elif attachment.get('type') == 'image':
                f = open(attachment.get('file'), 'rb')
                part = MIMEImage(
                    f.read(),
                    attachment.get('mimeType'),
                    attachment.get('encoder'),
                    **attachment.get('param'))
            
            elif attachment.get('type') == 'audio':
                f = open(attachment.get('file'), 'rb')
                part = MIMEAudio(
                    f.read(),
                    attachment.get('mimeType'),
                    attachment.get('encoder'),
                    **attachment.get('param'))
            
            elif attachment.get('type') == 'base':
                f = open(attachment.get('file'), 'rb')
                part = MIMEBase(
                    attachment.get('mimeMain'),
                    attachment.get('mimeType'))
                part.set_payload(open(attachment.get('file'), "rb").read())
                attachment.get('encoder')(part)
                    
            elif attachment.get('type') == 'message':
                part = MIMEMessage(
                    attachment.get('msg'),
                    attachment.get('mimeType'))
                                    
            elif attachment.get('type') == 'text':
                if os.path.isfile(attachment.get('file')):
                    f = open(attachment.get('file'), 'rb')
                    part = MIMEText(
                        f.read(),
                        attachmentEncoders.encode_base64.get('mimeType'),
                        attachment.get('charset'))
                        
                else:
                    part = MIMEText(
                        attachment.get('file'),
                        attachment.get('mimeType'),
                        attachment.get('charset'))
            
            if part:            
                if attachment.get('disposition') and f:
                    part.add_header('Content-Disposition', 'attachment; filename="' + f.name + '"')
                    
                self.__message.attach(part)

            if f:
                f.close()

        return self.__message
