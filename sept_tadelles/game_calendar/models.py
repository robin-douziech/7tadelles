from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

class Lieu(models.Model) :

	name = models.CharField(verbose_name="Nom du lieu", max_length=50, null=True, blank=True)

	adresse = models.CharField(verbose_name="Adresse", max_length=200, null=True, blank=True)
	complement = models.CharField(verbose_name="Complément d'adresse", max_length=50, null=True, blank=True)
	code_postal = models.CharField(verbose_name="Code postal", max_length=5, validators=[RegexValidator('^[0-9]{5}$')], null=True, blank=True)
	ville = models.CharField(verbose_name="Ville", max_length=50, null=True, blank=True)
	pays = models.CharField(verbose_name="Pays", max_length=50, null=True, blank=True)

	image = models.ImageField(verbose_name="Image", upload_to="photos/", null=True, blank=True)

	def __str__(self) :
		return self.name

class Soiree(models.Model) :

	lieu = models.ForeignKey(Lieu, verbose_name="Lieu", on_delete=models.CASCADE)
	date = models.DateTimeField(verbose_name="Date", null=True, blank=True)
