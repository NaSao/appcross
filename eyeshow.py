# [START imports]
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2
import uuid
from google.appengine.api import images


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
DISCOUNTOR_INFO = 'discountor_info'
DISCOUNT_LOG = 'discount_log'
url = 'https://mystical-healer-168312.appspot.com/'

# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.


# def url_add_params(url, **params):
#     '''add new params to web url'''
#     pr = urlparse.urlparse(url)
#     query = dict(urlparse.parse_qsl(pr.query))
#     query.update(params)
#     prlist = list(pr)
#     prlist[4] = urllib.urlencode(query)
#     return urlparse.ParseResult(*prlist).geturl()


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
    discountor = ndb.StructuredProperty(Discountor)
    originalPrice = ndb.StringProperty(indexed=False)
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
        
#         if discountorX is None:
#             template = JINJA_ENVIRONMENT.get_template('register.html')
#             self.response.write(template.render(template_values))
#         else:
#             template = JINJA_ENVIRONMENT.get_template('price.html')
#             self.response.write(template.render(template_values))

        template = JINJA_ENVIRONMENT.get_template('register.html')
        self.response.write(template.render(template_values))
        
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
        print discountor+"========================"
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
#         uuid = uuid.uuid5(uuid.NAMESPACE_DNS, 'crossmode')
        discountorOpenid = self.request.get('discountorOpenid')
        print discountorOpenid+"++++++++++++++++++"
        discountinfo = DiscountInfo()
#         discountinfo.uuid=uuid
        discountinfo.discountor=discountorOpenid
        discountinfo.originalPrice=price
#         discountinfo.put()
        #save discount info end
        
        
        #show qrcode start

        #show qrcode end
    
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
