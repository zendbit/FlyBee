import smtplib, os, imaplib
import pickle
import socket
import email

from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.message import MIMEMessage
from email.mime.base import MIMEBase
from email import encoders
from email.parser import HeaderParser
from smtplib import SMTP, SMTP_SSL
from imaplib import IMAP4, IMAP4_SSL
from ssl import SSLContext
from appconfig import AppConfig
from pickle import Pickler, Unpickler
from copy import deepcopy


class SMTPConnect():
    CODE_OK = 'ok'
    CODE_FAIL = 'fail'

    def __init__(self, config):
        appConfig = AppConfig().smtpOptions()
        self.__config = appConfig.get(config)
        

    def connect(self):
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

        smtpConfig = self.__config
        if smtpConfig:
            ssl = smtpConfig.get('ssl')
            server = smtpConfig.get('server')
            user = smtpConfig.get('user')
            password = smtpConfig.get('password')

            if ssl and ssl.get('certfile') and ssl.get('keyfile'):
                port = smtpConfig.get('port') if smtpConfig.get('port') else smtplib.SMTP_SSL_PORT

                outputMessage = self.__connectSMTPSSL(server, port, user, password, certfile=ssl.get('certfile'), keyfile=ssl.get('keyfile'), sslpassword=ssl.get('password'))

            else:
                port = smtpConfig.get('port') if smtpConfig.get('port') else smtplib.SMTP_PORT
                outputMessage = self.__connectSMTP(server, port, user, password)

                if outputMessage.get('code') == SMTPConnect.CODE_FAIL:
                    port = smtpConfig.get('port') if smtpConfig.get('port') else smtplib.SMTP_SSL_PORT
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
            self.__smtp = SMTP(host, port, timeout=10)
            self.__smtp.login(user, password)
            outputMessage['code'] = SMTPConnect.CODE_OK
            outputMessage['message'] = 'Success connected to {} {}'.format(host, port)

        except Exception as ex:
            outputMessage['message'] = 'Failed {}'.format(ex)

        return outputMessage

    
    def __connectSMTPSSL(self, host, port, user, password, certfile=None, keyfile=None, sslpassword=None):
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
            sslContext = None
            if certfile and keyfile:
                sslContext = SSLContext()
                sslContext.load_cert_chain(certfile, keyfile, sslpassword)

            self.__smtp = SMTP_SSL(host, port, context=sslContext, timeout=10)
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
            self.__smtp.send_message(messageBuilder)
            outputMessage['code'] = SMTPConnect.CODE_OK
            outputMessage['message'] = 'Success sending message'

        except Exception as ex:
            outputMessage['message'] = 'Failed sending message {}'.format(ex)

        finally:
            messageBuilder.clear()

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


    def clear(self):
        self.__message = MIMEMultipart()
        self.__messageAttachment.clear()
        self.__rcptOptions.clear()
        self.__mailOptions.clear()


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

            
    def attachApplication(self, filePath, mimeType='octet-stream', encoder=encoders.encode_base64, disposition=True, **params):
        '''
            attach application
            example:
                attachApplication('/home/amru/timesheet.xlsx')
        '''

        self.__messageAttachment.append({
                'file':filePath,
                'mimeType':mimeType,
                'encoder':encoder,
                'param':params,
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
                'param':params,
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


    def attachAudio(self, filePath, mimeType=None, encoder=encoders.encode_base64, disposition=True, **params):
        '''
            attach audio
            example:
                attachAudio('/home/amru/timesheet.ogg')
        '''

        self.__messageAttachment.append({
                'file':filePath,
                'mimeType':mimeType,
                'encoder':encoder,
                'param':params,
                'disposition':disposition,
                'type':'audio'
            })
            
        return self


    def attachBase(self, filePath, mimeMain='application', mimeType='octet-stream', encoder=encoders.encode_base64, disposition=True, **params):
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
                'param':params,
                'disposition':disposition,
                'type':'base'
            })

        return self

        
    def create(self):
        '''
            create message to send with send message
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

        message = deepcopy(self.__message)
        self.clear()

        return message


# override imap object to add timeout fuctionality
class IMAPObject(IMAP4):

    def __init__(self, host='', port=imaplib.IMAP4_PORT, timeout=None):
        self.timeout = timeout
        # no super(), it's an old-style class
        imaplib.IMAP4.__init__(self, host, port)

    
    def _create_socket(self):
        return socket.create_connection((self.host, self.port), timeout=self.timeout)


    def open(self, host='', port=imaplib.IMAP4_PORT):
        '''Setup connection to remote server on 'host:port'
            (default: localhost:standard IMAP4 port).
        This connection will be used by the routines:
            read, readline, send, shutdown.
        '''
        self.host = host
        self.port = port
        self.sock = self._create_socket()
        self.file = self.sock.makefile('rb')


# override imap object to add timeout fuctionality
class IMAPSSLObject(IMAP4_SSL):

    def __init__(self, host='', port=imaplib.IMAP4_SSL_PORT, ssl_context=None, timeout=None):
        self.timeout = timeout
        # no super(), it's an old-style class
        imaplib.IMAP4_SSL.__init__(self, host, port, ssl_context=ssl_context)


    def _create_socket(self):
        sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
        return self.ssl_context.wrap_socket(sock, server_hostname=self.host)


    def open(self, host='', port=imaplib.IMAP4_SSL_PORT):
        '''Setup connection to remote server on 'host:port'
            (default: localhost:standard IMAP4 port).
        This connection will be used by the routines:
            read, readline, send, shutdown.
        '''
        self.host = host
        self.port = port
        self.sock = self._create_socket()
        self.file = self.sock.makefile('rb')


class IMAPConnect():

    CODE_OK = 'ok'
    CODE_FAIL = 'fail'


    def __init__(self, config):
        self.__imapOptions = {
            'mailer_1':{
                'server':'imap.gmail.com',
                'port':None,
                'user':'amru.rosyada@gmail.com',
                'password':'tigerbrave86googlegmail',
                'ssl':{
                    'certfile':None,
                    'keyfile':None,
                    'password':None
                },
                'data_dir':os.path.sep.join((os.getcwd(), 'cached_data', 'mail'))
            }
        }

        self.__config = self.__imapOptions.get(config)
        self.__dataDir = os.path.sep.join((self.__config.get('data_dir'), self.__config.get('user')))


    def connect(self):
        '''
        server is config name set on _imapOptions
        return {
            'code':CODE_,
            'message:''
        }
        '''
        
        outputMessage = {
            'code':IMAPConnect.CODE_FAIL,
            'message':None
        }

        imapConfig = self.__config
        if imapConfig:
            ssl = imapConfig.get('ssl')
            server = imapConfig.get('server')
            user = imapConfig.get('user')
            password = imapConfig.get('password')

            if ssl and ssl.get('certfile') and ssl.get('keyfile'):
                port = imapConfig.get('port') if imapConfig.get('port') else imaplib.IMAP4_SSL_PORT
                outputMessage = self.__connectIMAPSSL(server, port, user, password, certfile=ssl.get('certfile'), keyfile=ssl.get('keyfile'), sslpassword=ssl.get('password'))

            else:
                port = imapConfig.get('port') if imapConfig.get('port') else imaplib.IMAP4_PORT
                outputMessage = self.__connectIMAP(server, port, user, password)

                if outputMessage.get('code') == SMTPConnect.CODE_FAIL:
                    port = imapConfig.get('port') if imapConfig.get('port') else imaplib.IMAP4_SSL_PORT
                    outputMessage = self.__connectIMAPSSL(server, port, user, password)

        else:
            outputMessage['message'] = 'imap configuration for {} not found'.format(config)

        return outputMessage


    def quit(self):

        outputMessage = {
            'code':IMAPConnect.CODE_OK,
            'message':'Quit imap session'
        }

        if self.__imap:
            try:
                self.__imap.logout()

            except Exception as ex:
                outputMessage['message'] = 'Failed when quit the imap session {}'.format(ex)

        return outputMessage


    def __connectIMAP(self, host, port, user, password):
        '''
        return
        {
            'code':CODE_,
            'message':''
        }
        '''

        outputMessage = {
            'code':IMAPConnect.CODE_FAIL,
            'message':None
        }

        try:
            self.__imap = IMAPObject(host, port, timeout=3)
            self.__imap.login(user, password)
            outputMessage['code'] = IMAPConnect.CODE_OK
            outputMessage['message'] = 'Success connected to {} {}'.format(host, port)

        except Exception as ex:
            outputMessage['message'] = 'Failed {}'.format(ex)

        return outputMessage

    
    def __connectIMAPSSL(self, host, port, user, password, certfile=None, keyfile=None, sslpassword=None):
        '''
        return
        {
            'code':CODE_,
            'message':''
        }
        '''

        outputMessage = {
            'code':IMAPConnect.CODE_FAIL,
            'message':None
        }

        try:
            sslContext = None
            if certfile and keyfile:
                sslContext = SSLContext()
                sslContext.load_cert_chain(certfile, keyfile, sslpassword)
                
            self.__imap = IMAPSSLObject(host, port, ssl_context=sslContext, timeout=3)
            self.__imap.login(user, password)
            outputMessage['code'] = IMAPConnect.CODE_OK
            outputMessage['message'] = 'Success connected to {} {}'.format(host, port)

        except Exception as ex:
            outputMessage['message'] = 'Failed {}'.format(ex)

        return outputMessage


    def unserializeEmailFromFile(self, emailId):
        '''
            unserialize json from email cache to variable
            outputMessage = {
                'code':IMAPConnect.CODE_FAIL,
                'message':None
                'data':None
            }
        '''
        
        outputMessage = {
            'code':IMAPConnect.CODE_FAIL,
            'message':None,
            'data':None
        }

        try:
            dirPath = os.path.sep.join((self.__dataDir, emailId))
            os.makedirs(dirPath, exist_ok=True)
            filePath = os.path.sep.join((dirPath, emailId))
            f = open(filePath, 'rb')
            content = Unpickler(f).load()
            f.close()
            outputMessage['code'] = IMAPConnect.CODE_OK
            outputMessage['message'] = 'Succsess load {}'.format(filePath)
            outputMessage['data'] = content
                
        except Exception as ex:
            outputMessage['message'] = ex

        return outputMessage


    def serializeEmailToFile(self, emailData):
        '''
            emailData = {
                'Subject':'',
                'CC':'',
                'BCC':'',
                'Attachment':[],
                'InlineAttachment':[],
                'ID':''
            }

            outputMessage = {
                'code':IMAPConnect.CODE_FAIL,
                'message':None
                'data':None
            }
        '''
        
        outputMessage = {
            'code':IMAPConnect.CODE_FAIL,
            'message':None,
            'data':None
        }

        try:
            emailId = emailData.get('id')
            dirPath = os.path.sep.join((self.__dataDir, emailId))
            os.makedirs(dirPath, exist_ok=True)
            filePath = os.path.sep.join((dirPath, emailId))
            f = open(filePath, 'wb')
            Pickler(f, protocol=pickle.HIGHEST_PROTOCOL).dump(emailData)
            f.close()
            outputMessage = self.unserializeEmailFromFile(emailId)
            
        except Exception as ex:
            outputMessage['message'] = ex

        return outputMessage


    def mailboxList(self):
        '''
            return list of mailbox list
            directory default to top level
            pattern default match to any

            outputMessage = {
                'code':IMAPConnect.CODE_,
                'message':'',
                'data':[] => list of mailbox if error None
            }
        '''
        
        outputMessage = {
            'code':IMAPConnect.CODE_FAIL,
            'message':None,
            'data':None
        }
        
        try:
            status, msg = self.__imap.list()
            msg = [mailbox.decode('UTF-8') for mailbox in msg]
            outputMessage['code'] = IMAPConnect.CODE_OK
            outputMessage['message'] = status
            outputMessage['data'] = msg

        except Exception as ex:
            outputMessage['message'] = ex
        
        return outputMessage


    def selectMailbox(self, mailbox='INBOX', readonly=False):
        '''
            select mailbox from imap object
            default is INBOX
            readonly True|False

            outputMessage = {
                'code':IMAPConnect.CODE_,
                'message':'',
                'data':None
            }
        '''
            
        outputMessage = {
            'code':IMAPConnect.CODE_FAIL,
            'message':None,
            'data':None
        }
        
        try:
            status, msg = self.__imap.select(mailbox, readonly)
            outputMessage['code'] = SMTPConnect.CODE_OK
            outputMessage['message'] = status
            outputMessage['data'] = msg

        except Exception as ex:
            outputMessage['message'] = ex
        
        return outputMessage


    def search(self, *criterion):
        '''
            do search in imap
            get email from imap object
            *criterion is for search criterion ex: 'FROM', '"LDJ"' or '(FROM "LDJ")'

            outputMessage = {
                'code':IMAPConnect.CODE_,
                'message':'',
                'data::None ==> if error default None, if success will return list of email id
            }
        '''
        
        outputMessage = {
            'code':IMAPConnect.CODE_FAIL,
            'message':None,
            'data':None
        }

        try:
            status, msg = self.__imap.uid('search', None, *criterion)
            
            emailIds = []
            if len(msg):
                msg_ids = msg[0].decode('UTF-8')
                if msg_ids != '':
                    emailIds = msg_ids.split(' ')

            outputMessage['code'] = IMAPConnect.CODE_OK
            outputMessage['message'] = status
            outputMessage['data'] = emailIds

        except Exception as ex:
            outputMessage['message'] = ex
        
        return outputMessage


    def fetch(self, emailId, *criterion):
        '''
            do fetch email information
            for specific emailId
            outputMessage = {
                'code':IMAPConnect.CODE_FAIL,
                'message':None,
                'data':None
            }
        '''
        
        outputMessage = {
            'code':IMAPConnect.CODE_FAIL,
            'message':None,
            'data':None
        }

        try:
            status, msg = self.__imap.uid('fetch', emailId, *criterion)
            outputMessage['code'] = IMAPConnect.CODE_OK
            outputMessage['message'] = status
            outputMessage['data'] = msg

        except Exception as ex:
            outputMessage['message'] = ex
        
        return outputMessage


    def storeCommand(self, message_id, command, flag_list):
        '''
            store imap flags
            command should be 'FLAGS', '+FLAGS', '-FLAGS', optionaly with suffix of ."SILENT".
            flag_list must be valid flag '\\Deleted', '\\Seen' etc
            outputMessage = {
                'code':IMAPConnect.CODE_FAIL,
                'message':None,
                'data':None
            }
        '''
        
        outputMessage = {
            'code':IMAPConnect.CODE_FAIL,
            'message':None,
            'data':None
        }

        try:
            status, msg = self.__imap.uid('STORE', message_id, command, flag_list)
            outputMessage['code'] = IMAPConnect.CODE_OK
            outputMessage['message'] = status
            outputMessage['data'] = msg

        except Exception as ex:
            outputMessage['message'] = ex
        
        return outputMessage


    def expunge(self):
        '''
            commit all change command to email
            should call this after change email flag
            outputMessage = {
                'code':IMAPConnect.CODE_FAIL,
                'message':None,
                'data':None
            }
        '''
        
        outputMessage = {
            'code':IMAPConnect.CODE_FAIL,
            'message':None,
            'data':None
        }

        try:
            status, msg = self.__imap.expunge()
            outputMessage['code'] = IMAPConnect.CODE_OK
            outputMessage['message'] = status
            outputMessage['data'] = msg

        except Exception as ex:
            outputMessage['message'] = ex
        
        return outputMessage


    def fetchHeader(self, emailId):
        '''
            get header of messages
            return parsed header messages
            parameter is emailId returned from serach result
            outputMessage = {
                'code':IMAPConnect.CODE_FAIL,
                'message':None,
                'data':None
            }
        '''
        
        outputMessage = {
            'code':IMAPConnect.CODE_FAIL,
            'message':None,
            'data':None
        }
        
        try:
            emailCache = self.unserializeEmailFromFile(emailId)
            if emailCache.get('code') == IMAPConnect.CODE_OK:
                outputMessage = emailCache

            else:
                emailInfo = self.fetch(emailId, '(BODY[HEADER])')
                if emailInfo.get('code') == IMAPConnect.CODE_OK:
                    header = emailInfo.get('data')[0][1].decode('UTF-8') #get header string then decode
                    parser = HeaderParser()
                    parsedHeader = parser.parsestr(header)

                    serializedEmail = {}
                    serializedEmail['id'] = emailId
                    serializedEmail['from'] = parsedHeader.get('From')
                    serializedEmail['to'] = parsedHeader.get('To')
                    serializedEmail['cc'] = parsedHeader.get('CC')
                    serializedEmail['bcc'] = parsedHeader.get('BCC')
                    serializedEmail['subject'] = parsedHeader.get('Subject')
                    serializedEmail['date'] = parsedHeader.get('Date')
                    self.serializeEmailToFile(serializedEmail)

                    outputMessage = self.unserializeEmailFromFile(emailId)

                else:
                    outputMessage = emailInfo

        except Exception as ex:
            outputMessage['code'] = IMAPConnect.CODE_FAIL
            outputMessage['message'] = ex
            outputMessage['data'] = None
            
        return outputMessage


    def fetchContent(self, emailId, download_attachment=False):
        '''
            get email content
            return email content with attachment filename
            outputMessage = {
                'code':IMAPConnect.CODE_FAIL,
                'message':None,
                'data':{
                    'content':'',
                    attachment:[
                        {'name':attachment01, 'mime':''},
                        {'name':attachment01, 'mime':''}
                    ],
                    inline_attachment:[
                        {'name':attachment01, 'mime':''},
                        {'name':attachment01, 'mime':''}
                    ]
                }
            }
        '''
        
        outputMessage = {
            'code':IMAPConnect.CODE_FAIL,
            'message':None,
            'data':None
        }

        try:
            dirPath = os.path.sep.join((self.__dataDir, emailId))
            
            # check serialize cache
            emailData = self.fetchHeader(emailId)
            if emailData.get('code') == IMAPConnect.CODE_OK:
                emailCache = emailData.get('data')

                if emailCache.get('text'):
                    outputMessage = emailData

                else:
                    emailCache['text'] = []
                    emailCache['attachment'] = []
                    emailCache['inline_attachment'] = []
                    emailCache['id'] = emailId
                    
                    body = self.fetch(emailId, '(BODY[])')
                    if body.get('code') == IMAPConnect.CODE_OK:
                        data = body.get('data')[0][1]
                        emailMsg = email.message_from_bytes(data)
                        
                        # check if download_attachment is set
                        for part in emailMsg.walk():
                            if part.get('Content-Disposition') and download_attachment:
                                # save attachment
                                filename = part.get_filename()
                                fp = open(filename, 'wb')
                                fp.write(part.get_payload(decode=True))
                                fp.close()
                                emailCache.get('attachment').append({'name':filename, 'mime':part.get_content_type()})
                                
                            # if plain text or html and not disposition
                            elif part.get_content_type() == 'text/plain' or part.get_content_type() == 'text/html':
                                body = part.get_payload(decode=True)
                                body = body.decode()
                                emailCache.get('text').append(body)
                                    
                            # else save as inline attachment
                            elif download_attachment:
                                # save attachment
                                filename = part.get_filename()
                                fp = open(cache_dir + os.path.sep + filename, 'wb')
                                fp.write(part.get_payload(decode=True))
                                fp.close()
                                # add attachment filename
                                emailCache.get('inline_attachment').append({'name':filename, 'mime':part.get_content_type()})
                                # append inline attachment value to content
                                emailCache.get('text').append('[pxemail:inline' + filename + ']')
                        
                        # make sure content is in text
                        #email_content['content'] = ''.join(email_content.get('content'))
                        emailCache['text'] = ''.join(emailCache.get('text'))
                        
                        self.serializeEmailToFile(emailCache)
                        outputMessage = self.fetchHeader(emailId)

        except Exception as ex:
            outputMessage['message'] = ex

        return outputMessage


class MessageFilterBuilder():
    '''
        this is filter builder that will return filter
        this filter is for retrieving email from imap protocol
    '''
    
    def __init__(self):
        self.__messageFilter = []


    def clear(self):
        self.__messageFilter.clear()

        
    def all(self):
        '''
            Returns all messages in the folder.
            You may run in to imaplib size limits if you request all the messages in a large folder.
            See Size Limits.
        '''
        
        self.__messageFilter.append('ALL')
        return self
        

    def before(self, date):
        '''
            These three search keys return, respectively,messages that were received by the IMAP server before given date.
            The date must be formatted like 05-Jul-2015.
        '''
        
        self.__messageFilter.append('BEFORE ' + date)
        return self
        

    def since(self, date):
        '''
            These three search keys return, respectively,messages that were received by the IMAP server since given date.
            The date must be formatted like 05-Jul-2015.
        '''
        
        self.__messageFilter.append('SINCE ' + date)
        return self
        

    def on(self, date):
        '''
            These three search keys return, respectively,messages that were received by the IMAP server on given date.
            The date must be formatted like 05-Jul-2015.
        '''
        
        self.__messageFilter.append('ON ' + date)
        return self
        

    def subject(self, text):
        '''
            add filter by subject that contain in text
            if text contain space add double quote:
            ex: '"amru rosyada"'
        '''
        
        self.__messageFilter.append('SUBJECT ' + text)
        return self
        

    def body(self, text):
        '''
            add filter that body contain in text
            if text contain space add double quote:
            ex: '"amru rosyada"'
        '''
        
        self.__messageFilter.append('BODY ' + text)
        return self
        

    def text(self, text):
        '''
            add filter that contain text
            if text contain space add double quote:
            ex: '"amru rosyada"'
        '''
        
        self.__messageFilter.append('TEXT ' + text)
        return self
        

    def sender(self, from_addr):
        '''
            add filter from address
            if more than one address should be user double quote
            '"amru.rosyada@gmail.com amru.rosyada@hotmail.com"'
        '''
        
        self.__messageFilter.append('FROM ' + from_addr)
        return self
        

    def ccTo(self, cc_addr):
        '''
            add filter bb address
            if more than one address should be user double quote
            '"amru.rosyada@gmail.com amru.rosyada@hotmail.com"'
        '''
        
        self.__messageFilter.append('CC ' + cc_addr)
        return self
        

    def bccTo(self, bcc_addr):
        '''
            add filter bcc address
            if more than one address should be user double quote
            '"amru.rosyada@gmail.com amru.rosyada@hotmail.com"'
        '''
        
        self.__messageFilter.append('BCC ' + bcc_addr)
        return self
        

    def seen(self):
        '''
            add filter seen
            filter all email with flag \Seen
        '''
        
        self.__messageFilter.append('SEEN')
        return self
        

    def unseen(self):
        '''
            add filter unseen
            filter all email without flag \Seen
        '''
        
        self.__messageFilter.append('UNSEEN')
        return self
        

    def answered(self):
        '''
            add filter answered
            Returns all messages with the \Answered flag
        '''
        
        self.__messageFilter.append('ANSWERED')
        return self
        

    def unanswered(self):
        '''
            add filter unanswered
            Returns all messages without the \Answered flag
        '''
        
        self.__messageFilter.append('UNANSWERED')
        return self
        

    def deleted(self):
        '''
            add filter deleted
            Returns all messages with the \Deleted flag
        '''
        
        self.__messageFilter.append('DELETED')
        return self
        

    def undeleted(self):
        '''
            add filter undeleted
            Returns all messages without the \Deleted flag
        '''
        
        self.__messageFilter.append('UNDELETED')
        return self
        

    def draft(self):
        '''
            add filter draft
            Returns all messages with the \Draft flag
        '''
        
        self.__messageFilter.append('DRAFT')
        return self
        

    def undraft(self):
        '''
            add filter undraft
            Returns all messages without the \Draft flag
        '''
        
        self.__messageFilter.append('UNDRAFT')
        return self
        

    def flagged(self):
        '''
            add filter flagged
            Returns all messages with the \Flagged flag
        '''
        
        self.__messageFilter.append('FLAGGED')
        return self
        

    def unflagged(self):
        '''
            add filter unflagged
            Returns all messages without the \Flagged flag
        '''
        
        self.__messageFilter.append('UNFLAGGED')
        return self
        

    def larger(self, n_bytes):
        '''
            add filter larger than n_bytes
        '''
        
        self.__messageFilter.append('LARGER')
        return self
        

    def smaller(self, n_bytes):
        '''
            add filter smaller than n_bytes
        '''
        
        self.__messageFilter.append('SMALLER')
        return self
        

    def nOt(self, search_key):
        '''
            Returns the messages that search-key would not have returned
        '''
        
        self.__messageFilter.append('NOT')
        return self
        

    def oR(self, search_key):
        '''
            Returns the messages that match either the first or second search-key
        '''
        
        self.__messageFilter.append('OR')
        return self
        

    def create(self):
        '''
            return all into list of filter
            then reset all value to empty
        '''
        
        criterion = ' '.join(self.__messageFilter).strip()
        self.clear()
        return criterion

