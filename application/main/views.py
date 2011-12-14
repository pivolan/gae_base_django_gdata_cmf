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

ACTS = [
	'',
	'1mFb0Jyvk3S56r_yneMWuGkG3ygpPLOVruN5gNPa_PVE',
  '1wDzyAjpJUpeKNyNaUn_kn4olYuT4OxHPoMgUpEYgciY',
  '1nHO5R2c8AYYr0zfr4SqggfzafiVxfMx2-6LJAKqA-xE',
  '1mZlvsom4FjxLKghLoV0hBy7uVvjMs9NoZlKa7C-34eo',
  '15g6msiv7uW2MZBcPdCaECiroDoxl6w1Lue-8YChzNsE',
  '1j0R0btcP7HULBINba1QVm1-i0fMNWvazn5C7f0fDQ9c',
  '1P9kltGeAVzL-PAgM4J4yKkUBSPr_zqw__Ki0uhhaLH4',
  '1hiFOdwuVK2h3q2FHoVRE2au0IpI8xvg3phpTV4F_G14',
]

@render_to("main/docs.html")
def index(request):
	return _get_doc('1V-yTMB6nFsXjE7LYjM9RbSETExPG0IrPnnYAayOQdEI')


@render_to("main/docs.html")
def offer(request):
	return _get_doc('1r1jdCGX6OIxOlmECXCYgQ3A_dqKH6oUhAxLZA6IKMr8')


@render_to("main/docs.html")
def acts(request, id = None):
	if id:
		id = int(id)
	if id and len(ACTS)>= id:
		return _get_doc(ACTS[id], False)
	else:
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


@render_to("main/docs.html")
def partners(request):
	return _get_doc('1zmIpDSiHQa2_N-oYGhvGiv_tGQaECktvaAw3J4gIDhE')


@render_to("main/license.html")
def license(request):
	return {}


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