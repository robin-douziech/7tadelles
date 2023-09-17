from django.db import models
import unidecode

from django.conf import settings



def image_name(instance, filename) :
	return f"wiki/games/{instance.short_name}/{instance.short_name}.png" 

def bg_image_name(instance, filename) :
	return f"wiki/games/{instance.short_name}/bg_{instance.short_name}.png" 

def rules_pdf_name(instance, filename) :
	return f"wiki/games/{instance.short_name}/{instance.short_name}.pdf" 



class Category(models.Model) :

	name = models.CharField(max_length=50)
	short_name = models.CharField(max_length=50)

	def __str__(self) :
		return self.name

class Game(models.Model) :

	name = models.CharField(max_length=50)
	short_name = models.CharField(max_length=50)

	has_image = models.BooleanField(default=False)
	image = models.ImageField(
		verbose_name = "Image",
		upload_to = image_name,
		null = True,
		blank = True
	)

	has_bg_image = models.BooleanField(default=False)
	bg_image = models.ImageField(
		verbose_name = "Background image",
		upload_to = bg_image_name,
		null = True,
		blank = True
	)

	bg_color = models.CharField(
		verbose_name = "Background color",
		max_length = 7,
		null = True,
		blank = True
	)

	players_min = models.IntegerField(default=0)
	players_max = models.IntegerField(default=0)
	duration = models.CharField(max_length=20, default="")
	age_min = models.IntegerField(default=0)

	description = models.TextField(default="")

	video_url = models.CharField(max_length=200, default="")

	#downloads_txt = models.CharField(max_length=200, default="")

	has_rules_pdf = models.BooleanField(default=False)
	rules_pdf = models.FileField(
		verbose_name = "PDF rules",
		upload_to=rules_pdf_name,
		null=True,
		blank=True
	)

	category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)

	def __init__(self, *args, **kwargs) :
		super(Game, self).__init__(*args, **kwargs)
		self.short_name = unidecode.unidecode(self.name.replace(" ", "_").lower())
		#self.has_image = self.image != None
		#self.has_bg_image = self.bg_image != None
		#self.has_rules_pdf = self.rules_pdf != None

	def save(self, *args, **kwargs) :
		self.short_name = unidecode.unidecode(self.name.replace(" ", "_").lower())
		#self.has_image = self.image != None
		#self.has_bg_image = self.bg_image != None
		#self.has_rules_pdf = self.rules_pdf != None
		super(Game, self).save(*args, **kwargs)

	def __str__(self) :
		return self.name