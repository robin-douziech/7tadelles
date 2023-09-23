from django import forms

from account import models
from soiree import models as soiree_models


class ProfileForm(forms.Form) :

	profile_photo = forms.ImageField(
		label = "Photo de profil",
		required = False
	)

	cover_photo = forms.ImageField(
		label = "Photo de couverture",
		required = False
	)

	def __init__(self, request, *args, **kwargs) :
		super(ProfileForm, self).__init__(*args, **kwargs)

class AddressForm(forms.Form) :

	adresse = forms.CharField(label="Adresse*", max_length=200)
	complement = forms.CharField(label="Complément d'adresse", max_length=200, required=False)
	code_postal = forms.CharField(label="Code postal*", max_length=5)
	ville = forms.CharField(label="Ville*", max_length=50)
	pays = forms.CharField(label="Pays*", max_length=50)
	image = forms.ImageField(label="Photo", required=False)

	def __init__(self, request, *args, **kwargs) :
		super(AddressForm, self).__init__(*args, **kwargs)
		if request.user.adresse is not None :
			self.fields['adresse'].initial = request.user.adresse.adresse
			self.fields['complement'].initial = request.user.adresse.complement
			self.fields['code_postal'].initial = request.user.adresse.code_postal
			self.fields['ville'].initial = request.user.adresse.ville
			self.fields['pays'].initial = request.user.adresse.pays

class TypeSoireeForm(forms.Form) :

	type_soiree_view = forms.MultipleChoiceField(
		label = "type de soirée view",
		choices = soiree_models.Soiree.TypeDeSoiree.choices,
		widget = forms.CheckboxSelectMultiple
	)

	type_soiree_notif = forms.MultipleChoiceField(
		label = "type de soirée notif",
		choices = soiree_models.Soiree.TypeDeSoiree.choices,
		widget = forms.CheckboxSelectMultiple
	)

	def __init__(self, request, *args, **kwargs) :
		super(TypeSoireeForm, self).__init__(*args, **kwargs)
		TYPES_SOIREE = [
			soiree_models.Soiree.TypeDeSoiree.PUB,
			soiree_models.Soiree.TypeDeSoiree.PUB_INSC,
			soiree_models.Soiree.TypeDeSoiree.PRIV_LIST_INSC,
			soiree_models.Soiree.TypeDeSoiree.PRIV_INVIT_CONFIRM
		]
		initial_view = []
		initial_notif = []
		for i in range(len(TYPES_SOIREE)) :
			if (request.user.parameters['type_soiree_view']//(2**i))%2 == 1:
				initial_view.append(TYPES_SOIREE[i])
			if (request.user.parameters['type_soiree_notif']//(2**i))%2 == 1:
				initial_notif.append(TYPES_SOIREE[i])

		self.fields['type_soiree_view'].initial = initial_view
		self.fields['type_soiree_notif'].initial = initial_notif


class NotifMailForm(forms.Form) :

	notif_mail = forms.BooleanField(label="Notif mail", required = False)

	def __init__(self, request, *args, **kwargs) :
		super(NotifMailForm, self).__init__(*args, **kwargs)
		self.fields['notif_mail'].initial = request.user.parameters['notif_mail']