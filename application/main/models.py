from google.appengine.ext import db
from django.contrib.auth import authenticate, login, logout
from django.contrib.syndication.feeds import Feed
from google.appengine.api import images
from google.appengine.api import users as googleUsers

#from appengine_admin.db_extensions import ManyToManyProperty

from django import forms
from django.utils.translation import ugettext as _

class Users(db.Model):
	uid = db.UserProperty()
	name = db.StringProperty()
	fio = db.StringProperty()
	company = db.StringProperty()
	phone = db.StringProperty()
	address = db.StringProperty()

class Pages(db.Model):
	pass