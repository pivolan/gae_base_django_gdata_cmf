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

from library.system.BeautifulSoup import BeautifulStoneSoup

import gdata.docs.data
import gdata.docs.client

import timeit
import re
import random
import datetime
from datetime import timedelta
import os

class view: pass

@render_to("main/index.html")
def index(request):
	return view.__dict__


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

def test(request):
	client = gdata.docs.client.DocsClient(source='yourCo-yourAppName-v1')
	client.ssl = True # Force all API requests through HTTPS
	client.http_client.debug = True # Set to True for debugging HTTP requests
	client.ClientLogin(settings.DOCS_EMAIL, settings.DOCS_PASS, client.source)

	view.entry = client.GetFileContent('/feeds/download/documents/Export?id=1ebCRp9Q0_7bxNwtAZr4XYC2sGOdXk3ij6kEpmi-P64Y&format=html')
	html = BeautifulStoneSoup(view.entry, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
	view.body = html.body.renderContents()
	view.style = html.style.prettify()
	return view.__dict__
