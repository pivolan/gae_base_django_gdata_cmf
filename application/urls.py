from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns("",
	(r"^$", "application.main.views.index"),

#	(r"^admin/", include("application.admin.urls")),
)