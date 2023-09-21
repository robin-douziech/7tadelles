import random, os
from account import models
import datetime as dt
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.contrib import admin as django_admin
from soiree import admin as soiree_admin
from soiree import models as soiree_models

def generate_token(length) :

	alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

	token = ""
	for i in range(length) :
		token += alphabet[random.randint(0, len(alphabet)-1)]

	return token

def find_user_by_email(email) :

	for user in models.User.objects.all() :
		if user.email == email :
			return user

	return None

def delete_media_file(path) :
	try :
		if os.path.isfile(path) :
			os.remove(path)
			return True
		else :
			return False
	except Exception as e :
		print(f"Erreur lors de la suppression d'un fichier media : {str(e)}")
		return False

def register_view(request, current_view, real_view, get_args="") :

	request.session['get_args'] = request.session.get('get_args', ["", ""])
	request.session['last_views'] = request.session.get('last_views', [['welcome:index', []], ['welcome:index', []]])
	if current_view != request.session['last_views'][1] :
		request.session['last_views'][0] = request.session['last_views'][1]
		request.session['get_args'][0] = request.session['get_args'][1]
		request.session['last_views'][1] = current_view
		request.session['get_args'][1] = get_args

	request.session['last_view'] = current_view
	if real_view :
		request.session['last_real_view'] = request.session.get('last_real_view', [])
		if len(request.session['last_real_view']) > 0 :
			if request.session['last_real_view'][-1] != current_view :
				request.session['last_real_view'].append(current_view)
		else :
			request.session['last_real_view'] = [current_view]

		if len(request.session['last_real_view']) > 10 :
			request.session['last_real_view'] = request.session['last_real_view'][-10:]

def send_notification(notification, users) :

	for user in users :
		notification.users.add(user)

		html = render_to_string('account/user/notification_mail.html', {'notification': notification})
		rcpt = [user.email for user in users]

		send_mail(
			subject="Nouvelle notification reçue",
			message="",
			from_email="info@7tadelles.com",
			recipient_list=rcpt,
			fail_silently=False,
			html_message=html,
		)



def week_day(date) :
	day_names = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
	return day_names[date.weekday()]

def month_str(date) :
	month_names = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
	return month_names[date.month-1]

def clean_user(user) :

	notifications_to_del = user.user_notifications.filter(created_at__lte=dt.datetime.now()-dt.timedelta(days=7))
	soirees_to_del = user.soirees_hote.filter(date__lte=dt.datetime.now()).union(user.invitations.filter(date__lte=dt.datetime.now()))
	
	for notification in notifications_to_del :
		notification.delete()
	for soiree in soirees_to_del :
		soiree.delete()

def get_actions(request) :
	actions = [('Modifier ma photo de profil', 'account:update_profile_photo', '', ())]
	if request.user.has_profile_photo :
		actions += [('Supprimer ma photo de profil', 'account:delete_profile_photo', '', ())]
	actions += [('Modifier ma photo de couverture', 'account:update_cover_photo', '', ())]
	if request.user.has_cover_photo :
		actions += [('Supprimer ma photo de couverture', 'account:delete_cover_photo', '', ())]
	actions += [('Modifier mon mot de passe', 'account:password_reset_email', '', ())]
	if request.user.adresse is not None :
		actions += [
			('Modifier mon adresse', 'account:change_address', '', ()),
			('Supprimer mon adresse', 'account:delete_address', '', ())
		]
	else :
		actions += [('Renseigner mon adresse', 'account:change_address', '', ())]
	if not(request.user.discord_verified) :
		actions += [('Lier mon compte discord', 'account:discord_verification_info', '', ())]
	if soiree_admin.SoireeAdmin(soiree_models.Soiree, django_admin.site).has_add_permission(request) :
		actions += [('Créer une soirée', 'soiree:creation_step_1', '', ())]
	actions += [('Rechercher utilisateur', 'account:list', '', ())]
	actions += [('Ajouter jeu', 'account:add_game', '', ())]
	return actions