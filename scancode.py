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





# [START main_page]
class MainPagescan(webapp2.RequestHandler):

    def post(self):
        duuid = self.request.get('uuid')
        template_values = {
        }
        
        template = JINJA_ENVIRONMENT.get_template('qcode.html')
        #self.response.write(template.render(template_values))

        
# [END main_page]

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
    ('/qcode', MainPagescan),
    ('/qcodei', QCode),
], debug=True)
# [END app]
