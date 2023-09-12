from django import forms
from django.core.validators import RegexValidator







class LieuCreationForm(forms.Form) :

	name = forms.CharField(label="Nom du lieu*", max_length=50)

	adresse = forms.CharField(label="Adresse*", max_length=200)
	complement = forms.CharField(label="Complément d'adresse", max_length=200, required=False)
	code_postal = forms.CharField(label="Code postal*", max_length=5, validators=[RegexValidator('^[0-9]{5}$')])
	ville = forms.CharField(label="Ville*", max_length=50)
	pays = forms.CharField(label="Pays*", max_length=50)
	image = forms.ImageField(label="Photo", required=False)

