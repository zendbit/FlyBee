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
        self._config = appConfig.get(config)
        

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

        smtpConfig = self._config
        if smtpConfig:
            ssl = smtpConfig.get('ssl')
            server = smtpConfig.get('server')
            user = smtpConfig.get('user')
            password = smtpConfig.get('password')

            if ssl and ssl.get('certfile') and ssl.get('keyfile'):
                port = smtpConfig.get('port') if smtpConfig.get('port') else smtplib.SMTP_SSL_PORT

                outputMessage = self._connectSMTPSSL(server, port, user, password, certfile=ssl.get('certfile'), keyfile=ssl.get('keyfile'), sslpassword=ssl.get('password'))

            else:
                port = smtpConfig.get('port') if smtpConfig.get('port') else smtplib.SMTP_PORT
                outputMessage = self._connectSMTP(server, port, user, password)

                if outputMessage.get('code') == SMTPConnect.CODE_FAIL:
                    port = smtpConfig.get('port') if smtpConfig.get('port') else smtplib.SMTP_SSL_PORT
                    outputMessage = self._connectSMTPSSL(server, port, user, password)

        else:
            outputMessage['message'] = 'smtp configuration for {} not found'.format(config)

        return outputMessage


    def quit(self):

        outputMessage = {
            'code':SMTPConnect.CODE_OK,
            'message':'Quit smtp session'
        }

        if self._smtp:
            try:
                self._smtp.quit()

            except Exception as ex:
                outputMessage['message'] = 'Failed when quit the smptp session {}'.format(ex)

        return outputMessage


    def _connectSMTP(self, host, port, user, password):
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
            self._smtp = SMTP(host, port, timeout=10)
            self._smtp.login(user, password)
            outputMessage['code'] = SMTPConnect.CODE_OK
            outputMessage['message'] = 'Success connected to {} {}'.format(host, port)

        except Exception as ex:
            outputMessage['message'] = 'Failed {}'.format(ex)

        return outputMessage

    
    def _connectSMTPSSL(self, host, port, user, password, certfile=None, keyfile=None, sslpassword=None):
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

            self._smtp = SMTP_SSL(host, port, context=sslContext, timeout=10)
            self._smtp.login(user, password)
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
            self._smtp.send_message(messageBuilder)
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
        
        self._message = MIMEMultipart()
        self._messageAttachment = []
        self._rcptOptions = []
        self._mailOptions = []


    def clear(self):
        self._message = MIMEMultipart()
        self._messageAttachment.clear()
        self._rcptOptions.clear()
        self._mailOptions.clear()


    def sender(self, sender):
        self._message['from'] = sender
        return self


    def sendTo(self, sendTo=[]):
        self._message['To'] = MessageBuilder.COMMASPACE.join(sendTo)
        return self


    def subject(self, subject):
        self._message['Subject'] = subject
        return self

        
    def ccTo(self, ccTo=[]):
        '''
            ccTo should be in list string of email address format
            ccTo = ['a@domain.com', 'b@domain.com']
        '''
        
        self._message['CC'] = MessageBuilder.COMMASPACE.join(ccTo)
        return self

        
    def bccTo(self, bccTo=[]):
        '''
            bccTo should be in list string of email address format
            bccTo = ['a@domain.com', 'b@domain.com']
        '''
        
        self._message['BCC'] = MessageBuilder.COMMASPACE.join(bccTo)
        return self

        
    def mailOptions(self, mailOptions=[]):
        '''
            add mail options
            options is like send_mail options
            see smtplib send_mail
            should be in list
        '''
        
        self._mailOptions = mailOptions
        return self

        
    def rcptOptions(self, rcptOptions=[]):
        '''
            add recepient options
            options is like send_mail options
            see smtplib send_mail
        '''
        
        self._rcptOptions = rcptOptions
        return self

            
    def attachApplication(self, filePath, mimeType='octet-stream', encoder=encoders.encode_base64, disposition=True, **params):
        '''
            attach application
            example:
                attachApplication('/home/amru/timesheet.xlsx')
        '''

        self._messageAttachment.append({
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

        self._messageAttachment.append({
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

        self._messageAttachment.append({
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

        self._messageAttachment.append({
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

        self._messageAttachment.append({
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

        self._messageAttachment.append({
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

        for attachment in self._messageAttachment:
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
                    
                self._message.attach(part)

            if f:
                f.close()

        message = deepcopy(self._message)
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
        appConfig = AppConfig().imapOptions()
        self._config = appConfig.get(config)
        self._dataDir = os.path.sep.join((self._config.get('data_dir'), self._config.get('user')))


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

        imapConfig = self._config
        if imapConfig:
            ssl = imapConfig.get('ssl')
            server = imapConfig.get('server')
            user = imapConfig.get('user')
            password = imapConfig.get('password')

            if ssl and ssl.get('certfile') and ssl.get('keyfile'):
                port = imapConfig.get('port') if imapConfig.get('port') else imaplib.IMAP4_SSL_PORT
                outputMessage = self._connectIMAPSSL(server, port, user, password, certfile=ssl.get('certfile'), keyfile=ssl.get('keyfile'), sslpassword=ssl.get('password'))

            else:
                port = imapConfig.get('port') if imapConfig.get('port') else imaplib.IMAP4_PORT
                outputMessage = self._connectIMAP(server, port, user, password)

                if outputMessage.get('code') == SMTPConnect.CODE_FAIL:
                    port = imapConfig.get('port') if imapConfig.get('port') else imaplib.IMAP4_SSL_PORT
                    outputMessage = self._connectIMAPSSL(server, port, user, password)

        else:
            outputMessage['message'] = 'imap configuration for {} not found'.format(config)

        return outputMessage


    def quit(self):

        outputMessage = {
            'code':IMAPConnect.CODE_OK,
            'message':'Quit imap session'
        }

        if self._imap:
            try:
                self._imap.logout()

            except Exception as ex:
                outputMessage['message'] = 'Failed when quit the imap session {}'.format(ex)

        return outputMessage


    def _connectIMAP(self, host, port, user, password):
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
            self._imap = IMAPObject(host, port, timeout=3)
            self._imap.login(user, password)
            outputMessage['code'] = IMAPConnect.CODE_OK
            outputMessage['message'] = 'Success connected to {} {}'.format(host, port)

        except Exception as ex:
            outputMessage['message'] = 'Failed {}'.format(ex)

        return outputMessage

    
    def _connectIMAPSSL(self, host, port, user, password, certfile=None, keyfile=None, sslpassword=None):
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
                
            self._imap = IMAPSSLObject(host, port, ssl_context=sslContext, timeout=3)
            self._imap.login(user, password)
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
            dirPath = os.path.sep.join((self._dataDir, emailId))
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
            dirPath = os.path.sep.join((self._dataDir, emailId))
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
            status, msg = self._imap.list()
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
            status, msg = self._imap.select(mailbox, readonly)
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
            status, msg = self._imap.uid('search', None, *criterion)
            
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
            status, msg = self._imap.uid('fetch', emailId, *criterion)
            outputMessage['code'] = IMAPConnect.CODE_OK
            outputMessage['message'] = 'OK'
            outputMessage['data'] = msg

        except Exception as ex:
            outputMessage['message'] = ex
        
        return outputMessage


    def storeCommand(self, emailId, command, flaglist):
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
            status, msg = self._imap.uid('STORE', emailId, command, flaglist)
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
            status, msg = self._imap.expunge()
            outputMessage['code'] = IMAPConnect.CODE_OK
            outputMessage['message'] = status
            outputMessage['data'] = msg

        except Exception as ex:
            outputMessage['message'] = ex
        
        return outputMessage


    def fetchHeader(self, emailId, overwrite=False):
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
            if emailCache.get('code') == IMAPConnect.CODE_OK and not overwrite:
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


    def fetchContent(self, emailId, downloadAttachment=False, overwrite=False):
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
            dirPath = os.path.sep.join((self._dataDir, emailId))
            
            # check serialize cache
            emailData = self.fetchHeader(emailId)
            if emailData.get('code') == IMAPConnect.CODE_OK:
                emailCache = emailData.get('data')

                if emailCache.get('text') and not overwrite:
                    outputMessage = emailData

                else:
                    print('download...')
                    emailCache['text'] = []
                    emailCache['html'] = []
                    emailCache['attachment'] = []
                    emailCache['inline_attachment'] = []
                    emailCache['id'] = emailId
                    
                    body = self.fetch(emailId, '(BODY[])')
                    if body.get('code') == IMAPConnect.CODE_OK:
                        data = body.get('data')[0][1]
                        emailMsg = email.message_from_bytes(data)
                        
                        # check if downloadAttachment is set
                        for part in emailMsg.walk():
                            if part.get('Content-Disposition') and downloadAttachment:
                                # save attachment
                                filename = part.get_filename()
                                if filename:
                                    fp = open(filename, 'wb')
                                    fp.write(part.get_payload(decode=True))
                                    fp.close()
                                    emailCache.get('attachment').append({'name':filename, 'mime':part.get_content_type()})
                                
                            # if plain text or html and not disposition
                            elif part.get_content_type() == 'text/plain':
                                body = part.get_payload(decode=True)
                                body = body.decode()
                                emailCache.get('text').append(body)

                            elif part.get_content_type() == 'text/html':
                                body = part.get_payload(decode=True)
                                body = body.decode()
                                emailCache.get('html').append(body)
                                    
                            # else save as inline attachment
                            elif downloadAttachment:
                                # save attachment
                                filename = part.get_filename()
                                if filename:
                                    fp = open(dirPath + os.path.sep + filename, 'wb')
                                    fp.write(part.get_payload(decode=True))
                                    fp.close()
                                    # add attachment filename
                                    emailCache.get('inline_attachment').append({'name':filename, 'mime':part.get_content_type()})
                                    # append inline attachment value to content
                                    emailCache.get('text').append('[pxemail:inline' + filename + ']')
                        
                        # make sure content is in text
                        #email_content['content'] = ''.join(email_content.get('content'))
                        emailCache['text'] = ''.join(emailCache.get('text'))
                        emailCache['html'] = ''.join(emailCache.get('html'))
                        
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
        self._messageFilter = []


    def clear(self):
        self._messageFilter.clear()

        
    def all(self):
        '''
            Returns all messages in the folder.
            You may run in to imaplib size limits if you request all the messages in a large folder.
            See Size Limits.
        '''
        
        self._messageFilter.append('ALL')
        return self
        

    def before(self, date):
        '''
            These three search keys return, respectively,messages that were received by the IMAP server before given date.
            The date must be formatted like 05-Jul-2015.
        '''
        
        self._messageFilter.append('BEFORE "{}"'.format(date))
        return self
        

    def since(self, date):
        '''
            These three search keys return, respectively,messages that were received by the IMAP server since given date.
            The date must be formatted like 05-Jul-2015.
        '''
        
        self._messageFilter.append('SINCE "{}"'.format(date))
        return self
        

    def on(self, date):
        '''
            These three search keys return, respectively,messages that were received by the IMAP server on given date.
            The date must be formatted like 05-Jul-2015.
        '''
        
        self._messageFilter.append('ON "{}"'.format(date))
        return self
        

    def subject(self, text):
        '''
            add filter by subject that contain in text
            if text contain space add double quote:
            ex: '"amru rosyada"'
        '''
        
        self._messageFilter.append('SUBJECT "{}"'.format(text))
        return self
        

    def body(self, text):
        '''
            add filter that body contain in text
            if text contain space add double quote:
            ex: '"amru rosyada"'
        '''
        
        self._messageFilter.append('BODY "{}"'.format(text))
        return self
        

    def text(self, text):
        '''
            add filter that contain text
            if text contain space add double quote:
            ex: '"amru rosyada"'
        '''
        
        self._messageFilter.append('TEXT "{}"'.format(text))
        return self
        

    def sender(self, from_addr):
        '''
            add filter from address
            if more than one address should be user double quote
            '"amru.rosyada@gmail.com amru.rosyada@hotmail.com"'
        '''
        
        self._messageFilter.append('FROM "{}"'.format(from_addr))
        return self
        

    def ccTo(self, cc_addr):
        '''
            add filter bb address
            if more than one address should be user double quote
            '"amru.rosyada@gmail.com amru.rosyada@hotmail.com"'
        '''
        
        self._messageFilter.append('CC "{}"'.format(cc_addr))
        return self
        

    def bccTo(self, bcc_addr):
        '''
            add filter bcc address
            if more than one address should be user double quote
            '"amru.rosyada@gmail.com amru.rosyada@hotmail.com"'
        '''
        
        self._messageFilter.append('BCC "{}"'.format(bcc_addr))
        return self
        

    def seen(self):
        '''
            add filter seen
            filter all email with flag \Seen
        '''
        
        self._messageFilter.append('SEEN')
        return self
        

    def unseen(self):
        '''
            add filter unseen
            filter all email without flag \Seen
        '''
        
        self._messageFilter.append('UNSEEN')
        return self
        

    def answered(self):
        '''
            add filter answered
            Returns all messages with the \Answered flag
        '''
        
        self._messageFilter.append('ANSWERED')
        return self
        

    def unanswered(self):
        '''
            add filter unanswered
            Returns all messages without the \Answered flag
        '''
        
        self._messageFilter.append('UNANSWERED')
        return self
        

    def deleted(self):
        '''
            add filter deleted
            Returns all messages with the \Deleted flag
        '''
        
        self._messageFilter.append('DELETED')
        return self
        

    def undeleted(self):
        '''
            add filter undeleted
            Returns all messages without the \Deleted flag
        '''
        
        self._messageFilter.append('UNDELETED')
        return self
        

    def draft(self):
        '''
            add filter draft
            Returns all messages with the \Draft flag
        '''
        
        self._messageFilter.append('DRAFT')
        return self
        

    def undraft(self):
        '''
            add filter undraft
            Returns all messages without the \Draft flag
        '''
        
        self._messageFilter.append('UNDRAFT')
        return self
        

    def flagged(self):
        '''
            add filter flagged
            Returns all messages with the \Flagged flag
        '''
        
        self._messageFilter.append('FLAGGED')
        return self
        

    def unflagged(self):
        '''
            add filter unflagged
            Returns all messages without the \Flagged flag
        '''
        
        self._messageFilter.append('UNFLAGGED')
        return self
        

    def create(self):
        '''
            return all into list of filter
            then reset all value to empty
        '''
        
        criterion = ' '.join(self._messageFilter).strip()
        self.clear()
        return criterion

