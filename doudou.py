# -*- coding: utf-8 -*-
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
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

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
        template = jinja_environment.get_template('register.html')
        self.response.out.write(template.render())

class Guestbook(webapp2.RequestHandler):
    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')
        name = self.request.get('name')
        self.redirect('/welcome/?' + urllib.urlencode({'name' : name, 'email' : email}))

class Login(webapp2.RequestHandler):
    def get(self):
        o = urlparse(self.request.uri).query
        params = parse_qs(o)

        template = jinja_environment.get_template('login.html')
        self.response.out.write(template.render())

class Register(webapp2.RequestHandler):
    def get(self):
        o = urlparse(self.request.uri).query
        params = parse_qs(o)

        template = jinja_environment.get_template('register.html')
        self.response.out.write(template.render())

app = webapp2.WSGIApplication([('/login', Login),
                               ('/', MainPage),
                               ('/register', Register)
                               ],
                              debug=True)