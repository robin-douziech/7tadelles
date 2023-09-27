from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse

from wiki import models as wiki_models
from account import models


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
	for joueur in models.User.objects.filter(discord_verified=True) :
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
		for joueur in models.User.objects.filter(discord_verified=True) :
			classement.append((joueur.username, stats[joueur.username]['global_score']))
		classement = sorted(classement, key=lambda x: x[1])[::-1]

	else :
		game = wiki_models.Game.objects.get(name=game_str)
		classement = sorted([(joueur.username, stats[joueur.username][game.name]['score']) for joueur in models.User.objects.filter(discord_verified=True)], key=lambda x: x[1])[::-1]

	return JsonResponse({
		'data': {
			'result': 'success',
			'classement': list(classement),
		}
	})

@bot_required
def get_score(request, bot_token) :

	game_str = request.GET.get('game', 'Général')
	discord_id = request.GET.get('id', False)

	if discord_id :

		try :
			user = models.User.objects.get(discord_id=discord_id)
		except :
			user = None

		if user is not None and user.discord_verified :

			score = 0

			if game_str == "Général" :
				for game in wiki_models.Game.objects.filter(ranking=True) :
					for partie in user.parameters['parties'][game.name] :
						score += 1.0*(partie[2]-(partie[1]-1))
						if partie[1] == 1 :
							score += 0.5*(partie[2]-(partie[1]-1))

			else :
				game = wiki_models.Game.objects.get(name=game_str)
				for partie in user.parameters['parties'][game.name] :
					score += 1.0*(partie[2]-(partie[1]-1))
					if partie[1] == 1 :
						score += 0.5*(partie[2]-(partie[1]-1))

			return JsonResponse({
			'data': {
				'result': 'success',
				'score': score,
			}
		})

		else :
			return JsonResponse({
			'data': {
				'result': 'failure',
				'error_msg': "Vous n'avez pas lié votre compte discord à votre compte sur 7tadelles.com"
			}
		})			

	else :
		return JsonResponse({
		'data': {
			'result': 'failure',
		}
	})
