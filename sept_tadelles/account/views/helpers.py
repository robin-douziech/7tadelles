import random, os
from account import models
import datetime as dt
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Q

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

def register_view(request, current_view) :

	request.session['last_views'] = request.session.get('last_views', [['welcome:index', []], ['welcome:index', []]])
	if current_view != request.session['last_views'][-1] :
		request.session['last_views'].append(current_view)

def send_notification(notification, users) :

	for user in users :
		notification.users.add(user)

		html = render_to_string('account/user/notification_mail.html', {'notification': notification})
		rcpt = [user.email for user in users]

		if user.parameters['notif_mail'] :
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

	# on supprime les notifications trop anciennes et les soirées passées
	notifications_to_del = user.user_notifications.filter(created_at__lte=dt.datetime.now()-dt.timedelta(days=7))
	soirees_to_del = user.soirees_hote.filter(date__lte=dt.datetime.now()).union(user.invitations.filter(date__lte=dt.datetime.now()))
	for notification in notifications_to_del :
		notification.delete()
	for soiree in soirees_to_del :
		soiree.delete()

	# on vérifie qu'il est bien invité à toutes les soirées publiques
	for soiree in soiree_models.Soiree.objects.filter(Q(type_soiree=soiree_models.Soiree.TypeDeSoiree.PUB_INSC) | Q(type_soiree=soiree_models.Soiree.TypeDeSoiree.PUB)) :
		if user not in soiree.invites.all() and user != soiree.hote :
			soiree.invites.add(user)
			soiree.save()
		if user not in soiree.notification_send_to.all() and user != soiree.hote :

			TYPES_SOIREE = [
				soiree_models.Soiree.TypeDeSoiree.PUB,
				soiree_models.Soiree.TypeDeSoiree.PUB_INSC,
				soiree_models.Soiree.TypeDeSoiree.PRIV_LIST_INSC,
				soiree_models.Soiree.TypeDeSoiree.PRIV_INVIT_CONFIRM
			]

			for i in range(len(TYPES_SOIREE)) :
				if soiree.type_soiree == TYPES_SOIREE[i] and (user.parameters['type_soiree_notif']//(2**i))%2 == 1 :
					notification = models.Notification(
						title = "Nouvelle invitation à une soirée jeux",
						text = f"{soiree.hote.username} vous invite à une soirée jeux le {week_day(soiree.date)} {soiree.date.day} {month_str(soiree.date)} {soiree.date.year}",
						link = "soiree:list",
						get_args = "",
						post_args = None,
						created_at = dt.datetime.now()
					)
					notification.save()
					send_notification(notification, [user])
					soiree.notification_send_to.add(user)
					soiree.save()

def get_actions(request) :
	actions = [('Mon profil', 'account:detail', f'?id={request.user.id}', ())]
	if soiree_admin.SoireeAdmin(soiree_models.Soiree, django_admin.site).has_add_permission(request) :
		actions += [('Nouvelle soirée', 'soiree:creation_step_1', '', ())]
	actions += [('Nouveau jeu', 'account:add_game', '', ())]
	if request.user.username == settings.SITE_OWNER_PSEUDO :
		actions += [('Nouvelle partie', 'leaderboard:partie_create', '', ())]
	if request.user.username == settings.SITE_OWNER_PSEUDO :
		actions += [('Parties en cours', 'leaderboard:partie_list', '?filter=open', ())]
	actions += [('Rechercher utilisateur', 'account:list', '', ())]
	if request.user.discord_verified :
		actions += [('Classements', 'leaderboard:index', '', ())]
	actions += [('Paramètres', 'account:parameters_base', '', ())]
	return actions