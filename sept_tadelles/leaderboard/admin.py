from django.contrib import admin
from django.conf import settings

from . import models

class PositionJoueurInline(admin.TabularInline):
    model = models.PositionJoueur
    extra = 0

@admin.register(models.Partie)
class PartieAdmin(admin.ModelAdmin) :
	filter_horizontal = ('joueurs',)
	list_display = ['jeu', 'finie']
	inlines = [PositionJoueurInline]

	def has_add_permission(self, request, obj=None) :
		return request.user.username == settings.SITE_OWNER_PSEUDO or request.user.is_superuser

	def has_view_permission(self, request, obj=None) :
		return request.user.username == settings.SITE_OWNER_PSEUDO or request.user.is_superuser

	def has_change_permission(self, request, obj=None) :

		if obj == None :
			return request.user.is_superuser
		else :
			return request.user.username == settings.SITE_OWNER_PSEUDO or request.user.is_superuser

	def has_del_permission(self, request, obj=None) :
		
		if obj == None :
			return request.user.is_superuser
		else :
			return request.user.username == settings.SITE_OWNER_PSEUDO or request.user.is_superuser

@admin.register(models.PositionJoueur)
class PositionJoueurAdmin(admin.ModelAdmin) :
	pass