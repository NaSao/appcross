# [START imports]
import os
import urllib2

from google.appengine.api import users
from google.appengine.ext import ndb
#from google.appengine.api import urlfetch

import jinja2
import webapp2
import uuid



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
    name = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
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
        user = users.get_current_user()
        email = user.email()
        discountorOpenid = email
        if duuid=="":
            template_values = {
             'discountorOpenid': discountorOpenid
            }
            discountorX = Discountor.query(Discountor.openid==discountorOpenid)
            
            if not discountorX.get():
                template = JINJA_ENVIRONMENT.get_template('register.html')
                self.response.write(template.render(template_values))
            else:
                template = JINJA_ENVIRONMENT.get_template('price.html')
                self.response.write(template.render(template_values))
        elif discountorOpenid=="" and duuid=="":
            template_values = {}
            template = JINJA_ENVIRONMENT.get_template('failpage.html')
            self.response.write(template.render(template_values))
        else:
            template_values = {
             'uuid' : duuid
             }
            discountinfoX = DiscountInfo.query(ndb.AND(DiscountInfo.duuid==duuid,DiscountInfo.state=='0'))
            if not discountinfoX.get():
                template = JINJA_ENVIRONMENT.get_template('failpage.html')
                self.response.write(template.render(template_values))
            else:
                for dis in discountinfoX:
                    dis.state="1"
                    dis.put()
                    
                template = JINJA_ENVIRONMENT.get_template('customerpage.html')
                self.response.write(template.render(template_values))
        
        

#         template = JINJA_ENVIRONMENT.get_template('register.html')
#         self.response.write(template.render(template_values))
        
# [END main_page]


# [START Register]
class Register(webapp2.RequestHandler):

    def post(self):
        discountorOpenid = self.request.get('discountorOpenid')
        discountor = Discountor()
        discountor.openid = discountorOpenid
        discountor.name = self.request.get('name')
        discountor.email = self.request.get('email')
        discountor.sex = self.request.get('sext')
        discountor.tel = self.request.get('area')+' '+self.request.get('tel')
        discountor.put()
        template_values = {
            'discountorOpenid': discountorOpenid
        }

        template = JINJA_ENVIRONMENT.get_template('price.html')
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
                
        self.response.out.write("<html><body style='text-align:center;'>")
        self.response.out.write('<div style="width:600px;margin-left:auto;margin-right:auto;"><img height="800" width="800" src="'+codeurl+'"></img></div>')
        self.response.out.write("</body></html>")
    
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
    ('/price', Register),
    ('/discount', Discounting),
], debug=True)
# [END app]
