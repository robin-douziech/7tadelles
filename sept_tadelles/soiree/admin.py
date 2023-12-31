from django.contrib import admin

from . import models


@admin.register(models.Soiree)
class SoireeAdmin(admin.ModelAdmin) :
	filter_horizontal = ('invites', 'notification_send_to', 'inscriptions')

	def has_add_permission(self, request, obj=None) :

		return request.user.adresse is not None or request.user.is_superuser

	def has_view_permission(self, request, obj=None) :

		if obj == None :
			return request.user.is_superuser
		else :
			return request.user in obj.invites.all() or obj in request.user.soirees_hote.all() or request.user.is_superuser

	def has_change_permission(self, request, obj=None) :

		if obj == None :
			return request.user.is_superuser
		else :
			return obj in request.user.soirees_hote.all() or request.user.is_superuser

	def has_del_permission(self, request, obj=None) :

		if obj == None :
			return request.user.is_superuser
		else :
			return obj in request.user.soirees_hote.all() or request.user.is_superuser