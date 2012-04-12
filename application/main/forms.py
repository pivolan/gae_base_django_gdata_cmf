__author__ = 'pivo'

from django import forms
from library.system.util import render_to_str

class feedback(forms.Form):
	fio = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	title = forms.CharField(required=True)
	text = forms.CharField(required=False, widget=forms.Textarea)

	@render_to_str('forms/feedback.html')
	def as_custom(self):
		return {'form': self}