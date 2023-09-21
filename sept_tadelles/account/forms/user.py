from django import forms
from django.core.validators import RegexValidator

from account import models

class UserSearchForm(forms.Form) :

	search = forms.CharField(label="Texte de la recherche", max_length=50, required=False)

	def __init__(self, request, *args, **kwargs) :
		super(UserSearchForm, self).__init__(*args, **kwargs)
		self.fields['search'].initial = request.GET.get('search', '')