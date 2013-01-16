import cgi
import datetime
import urllib
import webapp2
import jinja2
import os
from urlparse import urlparse, parse_qs

from google.appengine.ext import db
from google.appengine.api import users

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Greeting(db.Model):
    """Models an individual Guestbook entry with an author, content, and date."""
    author = db.StringProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

def guestbook_key(guestbook_name=None):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("""
            <html>
              <head>
                <meta charset="utf-8" />
              </head>
              <body>
                <header>doudou account number</header>
                <h1>welcome to doudou</h1>
                <div>
                  <form name="register" action="sign" method="post">
                    <div class="item"><label>   email</label><input type="text" name="email" maxlength="60" class="basic-input"></div>
                    <div class="item"><label>password</label><input type="password" name="password" maxlength="20" class="basic-input"></div>
                    <div class="item"><label>    name</label><input type="text" name="name" maxlength="15" class="basic-input"></div>
                    <input type="submit" value="regist" title="agree"/>
                  </form>
                </div>
                <footer></footer>
              </body>
            </html>
            """)

class Guestbook(webapp2.RequestHandler):
    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')
        name = self.request.get('name')
        self.redirect('/welcome/?' + urllib.urlencode({'name' : name, 'email' : email}))

class Welcome(webapp2.RequestHandler):
    def get(self):
        o = urlparse(self.request.uri).query
        params = parse_qs(o)

        self.response.out.write("""
            <html>
              <head>
                <meta charset="utf-8" />
              </head>
              <body>
                <h1>welcome to doudou</h1>
                <h2>%s(%s)</h2>
              </body>
            </html>
        """ % (params["name"], params["email"]))

app = webapp2.WSGIApplication([('/welcome/', Welcome),
                               ('/', MainPage),
                               ('/sign', Guestbook)
                               ],
                              debug=True)