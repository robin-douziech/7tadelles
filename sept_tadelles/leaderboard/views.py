from django.contrib import admin as django_admin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
import json

import datetime as dt

from . import forms, models, admin
from account.views import helpers

from wiki import models as wiki_models
from account import models as account_models

@login_required
def index(request) :

	if request.user.discord_verified :

		current_view = ['leaderboard:index', []]

		stats = {}
		classements = {
			"global": []
		}

		jeux = wiki_models.Game.objects.filter(ranking=True)
		joueurs = account_models.User.objects.filter(discord_verified=True)

		for joueur in account_models.User.objects.filter(discord_verified=True) :
			stats[joueur.username] = {
				'global_score': 0
			}
			for game in wiki_models.Game.objects.filter(ranking=True) :
				stats[joueur.username][game.name] = {
					'nb_parties': 0,
					'score': 0,
					**{str(position): 0 for position in range(1, game.players_max+1)},
				}
				for partie in joueur.parameters['parties'][game.name] :
					stats[joueur.username][game.name]['nb_parties'] += 1
					stats[joueur.username][game.name][str(partie[1])] += 1
					stats[joueur.username][game.name]['score'] += 1.0*(partie[2]-(partie[1]-1))
					if partie[1] == 1 :
						stats[joueur.username][game.name]['score'] += 0.5*(partie[2]-(partie[1]-1))
					stats[joueur.username]['global_score'] += stats[joueur.username][game.name]['score']

		for joueur in account_models.User.objects.filter(discord_verified=True) :
			classements['global'].append((joueur, stats[joueur.username]['global_score']))
		classements['global'] = sorted(classements['global'], key=lambda x: x[1])[::-1]

		for game in wiki_models.Game.objects.filter(ranking=True) :
			classements[game.name] = sorted([(joueur, stats[joueur.username][game.name]['score']) for joueur in account_models.User.objects.filter(discord_verified=True)], key=lambda x: x[1])[::-1]

		helpers.register_view(request, current_view)
		return render(request, 'leaderboard/index.html', {
			'jeux': jeux,
			'joueurs': joueurs,
			'classements': classements,
			'actions': helpers.get_actions(request),
		})

	else :
		return redirect('account:retour1')

@login_required
def reset_all_scores(request) :

	if request.user.username == settings.SITE_OWNER_PSEUDO :
		for joueur in account_models.User.objects.filter(discord_verified=True) :
			joueur.parameters.pop('parties')
			joueur.save()
	return redirect('account:retour1')

@login_required
def partie_list(request) :

	if admin.PartieAdmin(models.Partie, django_admin.site).has_view_permission(request) :

		filtre = request.GET.get('filter', 'all') # done, open, all
		current_view = [f"{reverse('leaderboard:partie_list')}?filter={filtre}", []]
		if filtre == 'all' :
			filtre = 'done+open'

		parties = models.Partie.objects.none()
		if 'done' in filtre :
			parties = parties.union(models.Partie.objects.filter(creator=request.user).filter(finie=True))
		if 'open' in filtre :
			parties = parties.union(models.Partie.objects.filter(creator=request.user).filter(finie=False))

		parties = parties.order_by("-created_at")

		helpers.register_view(request, current_view)
		return render(request, 'leaderboard/partie/list.html', {
			'parties': parties,
			'actions': helpers.get_actions(request),
		})

	else :
		return render(request, 'leaderboard/error.html', {'error_txt': "Vous n'avez pas la permission de voir les parties."})

@login_required
def partie_detail(request) :

	partie_id = request.GET.get('id', False)

	current_view = [f"{reverse('leaderboard:partie_detail')}{f'?id={partie_id}' if partie_id else ''}", []]

	if partie_id :

		try :
			partie = models.Partie.objects.get(pk=partie_id)
		except :
			partie = None

		positions = {joueur: 0 for joueur in partie.joueurs.all()}
		for joueur in partie.classement.all() :
			positions[joueur] = models.PositionJoueur.objects.get(partie=partie, joueur=joueur).position


		if admin.PartieAdmin(models.Partie, django_admin.site).has_change_permission(request, partie) :

			if not(partie.finie) :

				form = forms.PartieClassementForm(request, partie)
				if request.method == "POST" :
					form = forms.PartieClassementForm(request, partie, request.POST)
					if form.is_valid() :

						# on supprime les PositionJoueurs s'ils existent déjà
						positions_joueur = models.PositionJoueur.objects.filter(partie=partie)
						for position_joueur in positions_joueur :
							position_joueur.delete()
						
						# on range les joueurs dans l'ordre
						joueurs = []
						for i in range(1,len(partie.joueurs.all())+1) :
							for joueur in partie.joueurs.all() :
								if form.cleaned_data[f"{joueur}"] == i :
									joueurs.append(joueur)
						partie.joueurs.set(joueurs)
						partie.save()

						for joueur in partie.joueurs.all() :
							models.PositionJoueur.objects.create(partie=partie, joueur=joueur, position=form.cleaned_data[f"{joueur}"])
						
					return render(request, 'leaderboard/partie/detail_change.html', {
						'form': form,
						'partie': partie,
						'positions' :positions,
						'actions': helpers.get_actions(request),
					})

				helpers.register_view(request, current_view)
				return render(request, 'leaderboard/partie/detail_change.html', {
					'form': form,
					'partie': partie,
					'positions' :positions,
					'actions': helpers.get_actions(request),
				})

			else :

				helpers.register_view(request, current_view)
				return render(request, 'leaderboard/partie/detail_view.html', {
					'partie': partie,
					'positions' :positions,
					'actions': helpers.get_actions(request),
				})

		elif admin.PartieAdmin(models.Partie, django_admin.site).has_view_permission(request, partie) :

			helpers.register_view(request, current_view)
			return render(request, 'leaderboard/partie/detail_view.html', {
				'partie': partie,
				'positions' :positions,
				'actions': helpers.get_actions(request),
			})

		else :
			return render(request, 'leaderboard/error.html', {'error_txt': "Vous n'avez pas la permission de voir cette partie"})

	else :
		return redirect('account:retour1')


@login_required
def partie_terminer(request) :

	partie_id = request.GET.get('id', False)

	if partie_id :

		try :
			partie = models.Partie.objects.get(pk=partie_id)
		except :
			partie = None

		if admin.PartieAdmin(models.Partie, django_admin.site).has_change_permission(request, partie) :

			if not(partie.finie) :

				if len(partie.classement.all()) == len(partie.joueurs.all()) :

					for joueur in partie.classement.all() :
						position = models.PositionJoueur.objects.get(partie=partie, joueur=joueur).position
						joueur.parameters['parties'][partie.jeu.name].append((partie.id,position,len(partie.joueurs.all())))
						joueur.save()

					partie.finie = True
					partie.save()

	return redirect('account:retour1')

@login_required
def partie_annuler(request) :
	
	partie_id = request.GET.get('id', False)

	if partie_id :

		try :
			partie = models.Partie.objects.get(pk=partie_id)
		except :
			partie = None

		if admin.PartieAdmin(models.Partie, django_admin.site).has_change_permission(request, partie) :

			if partie.finie :

				for joueur in partie.classement.all() :
					for result in joueur.parameters['parties'][partie.jeu.name] :
						if result[0] == partie.id :
							joueur.parameters['parties'][partie.jeu.name].remove(result)
					joueur.save()

				partie.finie = False
				partie.save()

	return redirect('account:retour1')

@login_required
def partie_create(request) :

	current_view = ['leaderboard:partie_create', []]

	if request.user.username == settings.SITE_OWNER_PSEUDO :
		
		form = forms.PartieCreationForm()
		if request.method == "POST" :
			form = forms.PartieCreationForm(request.POST)
			if form.is_valid() :
				partie = models.Partie(
					creator = request.user,
					jeu = form.cleaned_data['jeu'],
					finie = False,
					created_at = dt.datetime.now()
				)
				partie.save()
				partie.joueurs.set(form.cleaned_data['joueurs'])
				partie.save()

				return redirect('account:retour1')

		#helpers.register_view(request, current_view)
		return render(request, 'leaderboard/partie/creation.html', {'form': form})

	else :
		return render(request, 'leaderboard/error.html', {'error_txt' : "Vous n'avez pas la permission de créer une Partie"})