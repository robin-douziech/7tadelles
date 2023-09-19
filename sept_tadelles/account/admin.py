from django.contrib import admin

from . import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin) :
	filter_horizontal = ('user_permissions', 'amis', 'demandes_envoyees')

	def has_add_permission(self, request, obj=None) :
		return True

	def has_view_permission(self, request, obj=None) :
		if obj == None :
			return request.user.is_superuser
		else :
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