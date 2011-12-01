from application.main.models import menuLeft

__author__ = 'pivo'


def menu_left(request):
	return {'menu_left': menuLeft.all()}
