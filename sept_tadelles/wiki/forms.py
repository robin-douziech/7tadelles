from django import forms
from django.core.validators import MinValueValidator

from . import models

class GameForm(forms.Form) :

	name = forms.CharField(
		label = "Name",
		max_length = 50
	)

	image = forms.ImageField(
		label = "Image",
		required = False
	)

	bg_image = forms.ImageField(
		label = "Background image",
		required = False
	)

	bg_color = forms.CharField(
		label = "Background color",
		required = False
	)

	players_min = forms.IntegerField(
		label = "Players min",
		validators = [MinValueValidator(1)],
		min_value = 1
	)

	players_max = forms.IntegerField(
		label = "Players max",
	)

	duration = forms.CharField(
		label = "Game duration",
		max_length = 15,
	)

	age_min = forms.IntegerField(
		label = "Minimum age",
		validators = [MinValueValidator(0)],
		min_value = 0
	)

	description = forms.CharField(
		label = "Description",
		max_length = 1000,
		widget = forms.Textarea()
	)

	video_url = forms.CharField(
		label = "Youtube vidéo ID",
		max_length = 15,
		initial = "none"
	)

	rules_pdf = forms.FileField(
		label = "Rules PDF",
		required = False
	)

	category = forms.ModelChoiceField(
		label = "Category",
		queryset = models.Category.objects.all()
	)

