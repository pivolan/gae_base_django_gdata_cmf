from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from google.appengine.api import users as googleUsers

def render_to(template):
	def renderer(function):
		def wrapper(request, *args, **kwargs):
			output = function(request, *args, **kwargs)
			if not isinstance(output, dict):
				return output
			tmpl = output.pop('TEMPLATE', template)
			return render_to_response(tmpl, output, context_instance=RequestContext(request))

		return wrapper

	return renderer


def render_to_str(template):
	def renderer(function):
		def wrapper(request, *args, **kwargs):
			output = function(request, *args, **kwargs)
			if not isinstance(output, dict):
				return output
			tmpl = output.pop('TEMPLATE', template)
			return render_to_string(tmpl, output, context_instance=RequestContext(request))

		return wrapper

	return renderer


class AuthenticationMiddleware(object):
	def process_request(self, request):
		assert hasattr(request,
		               'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."

		from auth import getCurrentUser

		request.user = getCurrentUser()
		from google.appengine.api import users

		request.is_admin = users.is_current_user_admin()
		return None


def login_required(redirect_to):
	def wrapper(fn):
		def login(request, id, **kwargs):
			output = fn(request, id, **kwargs)
			return output

		return login

	return wrapper


def admin_required(redirect_to):
	def wrapper(fn):
		def login(request, *kwarg, **kwargs):
			output = fn(request, *kwarg, **kwargs)
			if not googleUsers.is_current_user_admin():
				return HttpResponseRedirect(redirect_to=googleUsers.create_login_url(redirect_to))

			return output

		return login

	return wrapper


def permission_required(perm, login_url=None):
	"""
			Decorator for views that checks whether a user has a particular permission
			enabled, redirecting to the log-in page if necessary.
			"""
	return user_passes_test(lambda u: u.has_perm(perm), login_url=login_url)
