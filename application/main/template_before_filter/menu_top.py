from application.main.models import menuTop

__author__ = 'pivo'


def menu_top(request):
	return {'menu_top': menuTop.all()}
