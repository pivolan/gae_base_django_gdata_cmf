__author__ = 'pivo'

from django import forms
from library.system.util import render_to_str

class Feedback(forms.Form):
	company = forms.CharField(required=False)
	address = forms.CharField(required=True)
	phone = forms.CharField(required=True)
	fio = forms.CharField(required=False)
	email = forms.EmailField(required=True)
	title = forms.CharField(required=True)
	text = forms.CharField(required=False, widget=forms.Textarea)

	@render_to_str('forms/feedback.html')
	def as_custom(self):
		return {'form': self}