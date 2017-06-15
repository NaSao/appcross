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
url = 'https://mystical-healer-168312.appspot.com/'



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
    openid = ndb.StringProperty(indexed=False)
    originalPrice = ndb.StringProperty(indexed=False)
    state = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END discount]



# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        discountorOpenid = '1234456'
        template_values = {
             'discountorOpenid': discountorOpenid
        }
        discountorX = Discountor.query(Discountor.openid==discountorOpenid)
        
        if discountorX is None:
            template = JINJA_ENVIRONMENT.get_template('register.html')
            self.response.write(template.render(template_values))
        else:
            template = JINJA_ENVIRONMENT.get_template('price.html')
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

    def get(self):
        #save discount info start
        price = self.request.get('price')
        duuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'crossmode'))
        discountorOpenid = self.request.get('discountorOpenid')
        
        discountinfo = DiscountInfo()
        discountinfo.duuid=duuid
        discountinfo.openid=discountorOpenid
        discountinfo.originalPrice=price
        #0 is not used,1 is used
        discountinfo.state="0"
        discountinfo.put()
        #save discount info end
        url = QRCode_generator(duuid)
                
        self.response.out.write("<html><body>")
        self.response.out.write('<div style="width:600px;margin-left:auto;margin-right:auto;"><img height="200" width="200" src="'+url+'"></img></div>')
        self.response.out.write("</body></html>")
    
# [END Discounting]

# [START QCode]
class QCode(webapp2.RequestHandler):

    def post(self):
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
    ('/qcode', QCode),
], debug=True)
# [END app]
