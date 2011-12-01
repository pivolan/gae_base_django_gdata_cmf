from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns("",
	(r"^(.*)$", "application.admin.views.index"),
)