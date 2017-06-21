# -*- coding: utf-8 -*-
# [START imports]
import os
import urllib2

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import app_identity
from google.appengine.api import mail
#from google.appengine.api import urlfetch

import jinja2
import webapp2
import uuid
import socket
import string



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
DISCOUNTOR_INFO = 'discountor_info'
DISCOUNT_LOG = 'discount_log'
url = 'https://mystical-healer-168312.appspot.com'



def QRCode_generator(duuid):
        width = 200
        length = 200   
        data = url+'?uuid='+ duuid
        return 'http://chart.apis.google.com/chart?cht=qr'+'&chs='+ str(width)+'x' + str(length) + '&chl='+ data


# [START discount]
class Discountor(ndb.Model):
    openid = ndb.StringProperty(indexed=True)
    password = ndb.StringProperty(indexed=True)
    name = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=True)
    sex = ndb.StringProperty(indexed=False)
    tel = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    
class DiscountInfo(ndb.Model):
    duuid = ndb.StringProperty(indexed=True)
    openid = ndb.StringProperty(indexed=True)
    originalPrice = ndb.StringProperty(indexed=False)
    state = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END discount]



# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        duuid = self.request.get('uuid')
        if duuid=="":
            template_values = {}
            template = JINJA_ENVIRONMENT.get_template('login.html')
            self.response.write(template.render(template_values))
        else:
            discountinfoX = DiscountInfo.query(ndb.AND(DiscountInfo.duuid==duuid,DiscountInfo.state=='0'))
            print discountinfoX
            if not discountinfoX.get():
                template_values = {}
                template = JINJA_ENVIRONMENT.get_template('failpage.html')
                self.response.write(template.render(template_values))
            else:
                price = 0
                for dis in discountinfoX:
                    dis.state="1"
                    dis.put()
                    price = float(dis.originalPrice)*0.88
                    price = round(price,2)
                template_values = {
                 'price' : price
                }   
                template = JINJA_ENVIRONMENT.get_template('eyeshowpage.html')
                self.response.write(template.render(template_values))
        
# [END main_page]

# [START Login]
class Login(webapp2.RequestHandler):
    def post(self):
        semail = self.request.get('email')
        password = self.request.get('password')
        discountorX = Discountor.query(ndb.AND(Discountor.email==semail,Discountor.password==password))
        
        if not discountorX.get():
                message = 'no'
                template_values = {
                 'message': message
                }
                template = JINJA_ENVIRONMENT.get_template('login.html')
                self.response.write(template.render(template_values))
        else:
                template_values = {
                 'discountorOpenid': semail
                }
                template = JINJA_ENVIRONMENT.get_template('price.html')
                self.response.write(template.render(template_values))
# [END Login]

class PreRegister(webapp2.RequestHandler):
    def post(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('register.html')
        self.response.write(template.render(template_values))

# [START Register]
class Register(webapp2.RequestHandler):

    def post(self):
        semail = self.request.get('email')
        discountor = Discountor()
        discountor.openid = semail
        discountor.name = self.request.get('name')
        discountor.email = semail
        sext = self.request.get('sext')
        if sext is None or sext=="":
            discountor.sex = 'man' 
        else:
            discountor.sex=sext    
        discountor.password = self.request.get('password')
        tel = self.request.get('tel')
        area = self.request.get('area')
        discountor.tel = area+' '+tel
        discountorX = Discountor.query(Discountor.openid==semail)
        if not discountorX.get():
            discountor.put()
            template_values = {
                'discountorOpenid': semail                
            }
    
            template = JINJA_ENVIRONMENT.get_template('price.html')
            self.response.write(template.render(template_values))
        else:
            message = 'no'
            template_values = {
                'message': message,
                'email': semail,
                'name': discountor.name,
                'tel': tel,
                'sext': sext,
                'area': area
                }
            template = JINJA_ENVIRONMENT.get_template('register.html')
            self.response.write(template.render(template_values))
# [END Register]

# [START Discounting]
class Discounting(webapp2.RequestHandler):

    def post(self):
        #save discount info start
        price = self.request.get('price')
        duuid = str(uuid.uuid1())
        discountorOpenid = self.request.get('discountorOpenid')
        
        discountinfo = DiscountInfo()
        discountinfo.duuid=duuid
        discountinfo.openid=discountorOpenid
        discountinfo.originalPrice=price
        #0 is not used,1 is used
        discountinfo.state="0"
        discountinfo.put()
        #save discount info end
        codeurl = QRCode_generator(duuid)
        template_values = {
                'codeurl': codeurl
                }
        template = JINJA_ENVIRONMENT.get_template('qrcode.html')
        self.response.write(template.render(template_values))
#         self.response.out.write("<html><body style='text-align:center;'>")
#         self.response.out.write('<div style="margin-left:auto;margin-right:auto;"><img height="800" width="800" src="'+codeurl+'"></img></div>')
#         self.response.out.write("</body></html>")
    
# [END Discounting]


# [START Discounting]
class PreFindPass(webapp2.RequestHandler):
    
    def post(self):
        template_values = {                }
        template = JINJA_ENVIRONMENT.get_template('forgetpassword.html')
        self.response.write(template.render(template_values))
# [END Discounting]

# [START Discounting]
class FindPass(webapp2.RequestHandler):
    
    def post(self):
        email = self.request.get('email')
        discountorX = Discountor.query(Discountor.email==email)
        message = 'yes'
        if not discountorX.get():
            message = 'no'
        else:
            sender_address = (
                    'Example.com Support <{}@appspot.gserviceaccount.com>'.format(
                        app_identity.get_application_id()))
            subject = 'Eyeshow ϵͳ�һ�����'
            body = """�ǳ���л��ʹ��עCross Model ��ӭ���� Eyeshow ����
                      ���ĵ�½������ 
                       {}""".format(discountorX.get().password)
            mail.send_mail(sender_address, email, subject, body)
        
        template_values = {
            'message': message
        }
        template = JINJA_ENVIRONMENT.get_template('forgetpassword.html')
        self.response.write(template.render(template_values))
        
    
# [END Discounting]


# [START QCode]
class QCode(webapp2.RequestHandler):

    def post(self):
        duuid = self.request.get('uuid')
        template_values = {}
#         template_values = {
#             'user': user,
#             'greetings': greetings,
#             'guestbook_name': urllib.quote_plus(guestbook_name),
#             'url': url,
#             'url_linktext': url_linktext,
#         }
#       template = JINJA_ENVIRONMENT.get_template('register.html')
        template = JINJA_ENVIRONMENT.get_template('qcode.html')
        self.response.write(template.render(template_values))
# [END QCode]


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login',Login),
    ('/register',PreRegister),
    ('/price', Register),
    ('/discount', Discounting),
    ('/prefindpass', PreFindPass),
    ('/findpass', FindPass),
], debug=True)
# [END app]
