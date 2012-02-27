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


@render_to("main/docs.html")
def index(request, q=None):
	if q:
		return _get_doc_q(q)
	return _get_doc('1KCCoq3sGOpE6aMuoJMBoZzjNdLPEdGxgX23p40bOev4')


def _get_doc_q(q):
	q = q.encode('UTF-8')
	if googleUser.is_current_user_admin():
		memcache.delete(q)

	feeds = memcache.get(q)
	if not feeds:
		client = gdata.docs.client.DocsClient(source='yourCo-yourAppName-v1')
		client.ssl = True # Force all API requests through HTTPS
		client.http_client.debug = True # Set to True for debugging HTTP requests
		client.ClientLogin(settings.DOCS_EMAIL, settings.DOCS_PASS, client.source)
		feeds = client.GetDocList(
			uri='/feeds/default/private/full?title=%s&title-exact=true&max-results=1&showfolders=true' % q)
		memcache.add(q, feeds)

	for doc in feeds.entry:
		memcache.add(q, doc.resource_id.text.replace('document:', ''))
		folders = doc.InFolders()
		return _get_doc(doc.resource_id.text.replace('document:', ''), folders)
	return False


def _get_doc(id, folders = None):
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
		'body': body.replace('http:///','/'),
		'style': style,
		'id': id,
	  'folders':folders,
		}


def login(request):
	return HttpResponseRedirect(redirect_to=googleUsers.create_login_url(request.META['HTTP_REFERER']))


def logout(request):
	return HttpResponseRedirect(redirect_to=googleUsers.create_logout_url(request.META['HTTP_REFERER']))

@render_to('main/filesupload.html')
def filesupload(request):
	return {}