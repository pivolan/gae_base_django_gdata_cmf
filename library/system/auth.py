def auth(request):
	if hasattr(request, 'user'):
		user = request.user
	else:
		user = getCurrentUser()

	from google.appengine.api import users

	return {
		'user': user,
		'is_admin': users.is_current_user_admin()
	}


def getCurrentUser():
	from google.appengine.api import users
	from application.main.models import Users

	uid = users.get_current_user()
	user = False
	if uid:
		user = Users.all().filter('uid =', uid).get()
		if not user:
			user = Users(uid=uid)
			user.put()
	return user