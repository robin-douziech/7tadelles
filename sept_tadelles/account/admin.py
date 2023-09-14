from django.contrib import admin

from . import models

@admin.register(models.Soiree)
class SoireeAdmin(admin.ModelAdmin) :
	filter_horizontal = ('invites', 'notification_send_to', 'inscriptions')

	def has_add_permission(self, request, obj=None) :

		return request.user.adresse is not None or request.user.is_superuser

	def has_view_permission(self, request, obj=None) :

		if obj == None :
			return request.user.soirees_hote.exists() or request.user.invitations.exists() or request.user.is_superuser
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


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin) :
	filter_horizontal = ('user_permissions', 'amis', 'demandes_envoyees')

	def has_add_permission(self, request, obj=None) :
		return True

	def has_view_permission(self, request, obj=None) :
		return True

	def has_change_permission(self, request, obj=None) :
		if obj == None :
			return request.user.is_superuser
		else :
			return request.user.is_superuser or request.user == self

	def has_del_permission(self, request, obj=None) :
		if obj == None :
			return request.user.is_superuser
		else :
			return request.user.is_superuser or request.user == self

@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin) :
	filter_horizontal = ('users',)

admin.site.register(models.Lieu)