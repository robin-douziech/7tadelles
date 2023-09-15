import random, os
from account import models
from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string

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

def register_view(request, current_view, real_view) :

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

def clean_user(request) :

	notifications_to_del = request.user.user_notifications.filter(created_at__lte=dt.datetime.now()-dt.timedelta(days=7))
	soirees_to_del = request.user.soirees_hote.filter(date__lte=dt.datetime.now()).union(request.user.invitations.filter(date__lte=dt.datetime.now()))

	for notification in notifications_to_del :
		notification.delete()
	for soiree in soirees_to_del :
		soiree.delete()