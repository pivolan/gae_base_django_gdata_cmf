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
from application.main.forms import Feedback

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
		result = _get_doc(pages[id])
	result['menu_current'] = {id: 'id="current"'}
	return result


@render_to("main/license.html")
def license(request):
	return {'menu_current': {'lic': 'id="current"'}}


@render_to("main/contacts.html")
def contacts(request):
	id = 'con'
	result = _get_doc(pages[id])
	result['menu_current'] = {id: 'id="current"'}
	form = Feedback()
	if request.method == 'POST':
		form = Feedback(request.POST)
		if form.is_valid():
			mail.send_mail(sender=settings.ADMIN_EMAIL,
						   to=settings.ADMIN_EMAIL,
						   subject=form.cleaned_data['title'],
						   body=form.cleaned_data['text'] + ' ' + form.cleaned_data['email'])
			return HttpResponseRedirect('/contacts')

	result['form'] = {
		'feedback': form
	}
	return result


def _get_doc(id, use_cache = True):
	if googleUser.is_current_user_admin():
		memcache.delete(id)

	result = memcache.get(id)
	if not result:
		client = gdata.docs.client.DocsClient(source='yourCo-yourAppName-v1')
		client.ssl = True # Force all API requests through HTTPS
		client.http_client.debug = True # Set to True for debugging HTTP requests
		client.ClientLogin(settings.DOCS_EMAIL, settings.DOCS_PASS, client.source)

		entry = client.GetFileContent(
			'/feeds/download/documents/Export?id=%s&format=html' % id)
		html = BeautifulStoneSoup(entry, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)

		head_title = ''
		keywords = ''
		description = ''

		if html.body.div:
			head_title = html.body.div.find(text=re.compile("title = .*"))
			keywords = html.body.div.find(text=re.compile("keywords = .*"))
			description = html.body.div.find(text=re.compile("description = .*"))
		title = html.head.title.text

		if head_title:
			head_title = head_title.replace("title = ", '')
		else:
			head_title = title
		if keywords:
			keywords = keywords.replace("keywords = ", '')
		if description:
			description = description.replace("description = ", '')

		[divs.extract() for divs in html.body.findAll('div')]
		body = html.body.renderContents()
		style = html.style.prettify()

		result = {
			'entry':entry,
			'title': title,
		  'html':html,
			'body': body.replace('http:///','/'),
			'style': style,
			'id': id,
			'head_title': head_title,
			'keywords':keywords,
			'description':description,
			}
		if use_cache:
			memcache.add(id, result)
	return result


def login(request):
	return HttpResponseRedirect(redirect_to=googleUsers.create_login_url(request.META['HTTP_REFERER']))


def logout(request):
	return HttpResponseRedirect(redirect_to=googleUsers.create_logout_url(request.META['HTTP_REFERER']))