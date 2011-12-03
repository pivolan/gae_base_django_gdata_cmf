from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns("",
	(r"^$", "application.main.views.index"),
	(r"^acts$", "application.main.views.acts"),
	(r"^offer$", "application.main.views.offer"),
	(r"^contacts$", "application.main.views.contacts"),
	(r"^certification$", "application.main.views.certification"),
	(r"^energy$", "application.main.views.energy"),
	(r"^experience$", "application.main.views.experience"),

	(r"^acts/(\d*)$", "application.main.views.acts"),

	(r"^login$", "application.main.views.login"),
	(r"^logout$", "application.main.views.logout"),

#	(r"^admin/", include("application.admin.urls")),
)