from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse

from wiki import models as wiki_models
from account import models as account_models

def bot_required(function) :

	def valid_token(request, bot_token) :
		if bot_token == settings.BOT_TOKEN :
			return function(request, bot_token)
		else :
			return JsonResponse({
				'data': {
					'result': 'failure',
				},
			})

	return valid_token	


@bot_required
def get_ranking_games(request, bot_token) :
	games = wiki_models.Game.objects.filter(ranking=True)
	return JsonResponse({
		'data': {
			'result': 'success',
			'games': [game.name for game in games],
		},
	})

@bot_required
def get_classement(request, bot_token) :
	game_str = request.GET.get('game', 'Général')

	classement = []

	stats = {}
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

	if game_str == "Général" :
		for joueur in account_models.User.objects.filter(discord_verified=True) :
			classement.append((joueur.username, stats[joueur.username]['global_score']))
		classement = sorted(classement, key=lambda x: x[1])[::-1]

	else :
		game = wiki_models.Game.objects.get(name=game_str)
		classement = sorted([(joueur.username, stats[joueur.username][game.name]['score']) for joueur in account_models.User.objects.filter(discord_verified=True)], key=lambda x: x[1])[::-1]

	return JsonResponse({
		'data': {
			'result': 'success',
			'classement': list(classement),
		}
	})

@bot_required
def get_score(request, bot_token) :
	pass
