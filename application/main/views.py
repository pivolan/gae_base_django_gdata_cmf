from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from google.appengine.api import images

from pprint import pprint

from library.system.util import render_to
from application.main.models import *

from google.appengine.api import memcache
from google.appengine.api import mail
from google.appengine.api import users as googleUser

import timeit
import re
import random
import datetime
from datetime import timedelta
import os

@render_to("main/index.html")
def index(request):
	return {}


@render_to("main/offer.html")
def offer(request):
	return {}


@render_to("main/acts.html")
def acts(request):
	return {}

@render_to("main/contacts.html")
def contacts(request):
	return {}

@render_to("main/experience.html")
def experience(request):
	return {}

@render_to("main/certification.html")
def certification(request):
	return {}

@render_to("main/energy.html")
def energy(request):
	return {}
