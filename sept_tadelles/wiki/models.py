from django.db import models


class Category(models.Model) :

	name = models.CharField(max_length=50)
	short_name = models.CharField(max_length=50)

	def __str__(self) :
		return self.name

class Game(models.Model) :

	name = models.CharField(max_length=50)
	short_name = models.CharField(max_length=50)

	players_min = models.IntegerField(default=0)
	players_max = models.IntegerField(default=0)
	duration = models.CharField(max_length=20, default="")
	age_min = models.IntegerField(default=0)

	description = models.TextField(default="")

	video_url = models.CharField(max_length=200, default="")

	downloads_txt = models.CharField(max_length=200, default="")

	category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

	prochainement = models.BooleanField(default=False)

	def __str__(self) :
		return self.name