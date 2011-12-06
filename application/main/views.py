from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from google.appengine.api import images
from django.conf import settings

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

pages = {
	'about': '1xh1Z9py4oxUQiFleMTEV1SrkD8WkeXhUnZZ5z5Fv3Es',
	'equip': '1MwmVqkS_5vlup6r9X55XwSsfHIrvM6asCZm7VT25uAs',
	'exp': '1YC8tDpr2v203YvcTyaUTVL-EG6Jr0fbLYsyGqmU1Ai8',
	'lic': '1ZTlKRW7pWjJYrxuqYoyblbcR7vEXf9ubZLMY2WDgOI4',
	'offer': '1BsXsaNqPdjMXXxUTTfPdkYAn6yIAY9_55HLXw-lcrUI',
	'par': '1GaVeFdWIe5lxRqTA_JqVSBto1TDCBvzlGp83emtVyNc',
	'con': '1NX0BCGJDDV7-t-D3L_HXLP8D1wOnTssTENKScQnp9xQ',
	}

@render_to("main/docs.html")
def index(request, id='about'):
	result = {}
	if id in pages:
		result = _get_doc(pages[id])
	else:
		id = 'about'
	result = _get_doc(pages['about'])
	result['menu_current'] = {id: 'id="current"'}
	return result


def _get_doc(id):
	if googleUser.is_current_user_admin():
		memcache.delete(id)

	entry = memcache.get(id)
	if not entry:
		client = gdata.docs.client.DocsClient(source='yourCo-yourAppName-v1')
		client.ssl = True # Force all API requests through HTTPS
		client.http_client.debug = True # Set to True for debugging HTTP requests
		client.ClientLogin(settings.DOCS_EMAIL, settings.DOCS_PASS, client.source)

		entry = client.GetFileContent(
			'/feeds/download/documents/Export?id=%s&format=html' % id)
		memcache.add(id, entry)
	html = BeautifulStoneSoup(entry, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
	body = html.body.renderContents()
	style = html.style.prettify()
	return {
		'entry': entry,
		'title': html.head.title.text,
		'html': html,
		'body': body,
		'style': style,
		'id': id,
		}


def login(request):
	return HttpResponseRedirect(redirect_to=googleUsers.create_login_url(request.META['HTTP_REFERER']))


def logout(request):
	return HttpResponseRedirect(redirect_to=googleUsers.create_logout_url(request.META['HTTP_REFERER']))