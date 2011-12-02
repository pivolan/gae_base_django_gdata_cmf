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


@render_to("main/docs.html")
def index(request):
	return _get_doc('1V-yTMB6nFsXjE7LYjM9RbSETExPG0IrPnnYAayOQdEI')


@render_to("main/docs.html")
def offer(request):
	return _get_doc('1r1jdCGX6OIxOlmECXCYgQ3A_dqKH6oUhAxLZA6IKMr8')


@render_to("main/docs.html")
def acts(request):
	return _get_doc('1N82DHbYJQVy7ZA3IRzgtjqZnxIb08vCH0HpGeyaiKKU')


@render_to("main/contacts.html")
def contacts(request):
	result = _get_doc('1pjbpq1rRig1Nwmn7gwoyWH1lqBk1JkOp39xHcqY32KI')
	if request.method == "POST":
		form = feedback_form(request.POST)
		if form.is_valid():
			mail.send_mail(sender=form.cleaned_data['email'],
			               to=settings.ADMIN_EMAIL,
			               subject=form.cleaned_data['title'],
			               body=form.cleaned_data['text'])
			return HttpResponseRedirect('/contacts')
	else:
		initial_data = {}
		if request.user:
			user = request.user
			initial_data = {
				'company': user.company,
				'address': user.address,
				'phone': user.phone,
				'fio': user.fio,
				'email': user.email(),
				}
		form = feedback_form(initial=initial_data)
	result['form'] = form
	return result


@render_to("main/docs.html")
def experience(request):
	return _get_doc('19miGFML3p4KCgPWb_uUr12atBch5UoaZZ9KhPNOs3_o')


@render_to("main/docs.html")
def certification(request):
	return _get_doc('1Uthw7v7VGbMRRYhYkdHoSIz76pTQuZJBhSuWR-yXXVE')


@render_to("main/docs.html")
def energy(request):
	return _get_doc('1Yx0pbyKlCm6lBCoZ74OkESiz5UnWKsdzf3dryMqyA_8')


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