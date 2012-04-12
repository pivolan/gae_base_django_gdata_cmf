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
from application.main.forms import feedback as feedback_form

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

PAGES = {
	'main': '18VcZvV4_7nNxg4258Sn4UBx4HbTPXOlPg3qtkcmeaYI',
	'debt': '16AG7bjr10VOBePwjBg6YFiq6TZHP4y71VlzHnW6HJZs',
	'instruction': '1BWPNkoszVKLMYgcw2T7c7LfILECfhB7DtiuwyNxavtk',
	'coop': '12OjeSXWP26805u1sGzX3wPG1jMKghzQ4mK3qwEPiGv8',
	'donate': '1JX_FDVIGWdwziqvRsuXrHOzBdA3kjg740kka66geCu4',
	'contacts': '1R4OuInyiWTArzNUiHen2xXgq6pwPhhhY5TTJD2BK0BQ',
	'forum': '1Qo9EHd0_SCL2O17ffWzvfCrNAAB0_UZzppb9HwleBC8',
	}

@render_to("main/docs.html")
def index(request, page_name = 'main'):
	return _get_doc(PAGES[page_name])

@render_to("main/forum.html")
def forum(request):
	result = _get_doc(PAGES['forum'])
	if request.method == "POST":
		form = feedback_form(request.POST)
		if form.is_valid():
			request.session['status_feedback'] = 'mn,mn'
			mail.send_mail(sender=settings.ADMIN_EMAIL,
			               to=settings.ADMIN_EMAIL,
			               subject=form.cleaned_data['title'],
			               body=form.cleaned_data['text'] + form.cleaned_data['email'])
			return HttpResponseRedirect('/forum')
	else:
		initial_data = {}
		if request.user:
			user = request.user
			initial_data = {
				'fio': user.fio,
				'email': user.email(),
				}
		form = feedback_form(initial=initial_data)

	if 'status_feedback' in request.session:
		form.sended = True
		del(request.session['status_feedback'])
	else:
		form.sended = False

	result['form'] = form

	result['sended'] = True
	return result

def _get_doc(id, use_cache=True):
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
			'entry': entry,
			'title': title,
			'html': html,
			'body': body.replace('http:///', '/'),
			'style': style,
			'id': id,
			'head_title': head_title,
			'keywords': keywords,
			'description': description,
			}
		if use_cache:
			memcache.add(id, result)
	return result


def login(request):
	return HttpResponseRedirect(redirect_to=googleUsers.create_login_url(request.META['HTTP_REFERER']))


def logout(request):
	return HttpResponseRedirect(redirect_to=googleUsers.create_logout_url(request.META['HTTP_REFERER']))