from django.contrib import admin

from . import models

@admin.register(models.Game)
class GameAdmin(admin.ModelAdmin) :

	def has_add_permission(self, request, obj=None) :

		return request.user.is_superuser

	def has_view_permission(self, request, obj=None) :
		
		return True

	def has_change_permission(self, request, obj=None) :
		
		return request.user.is_superuser

	def has_del_permission(self, request, obj=None) :
		
		return request.user.is_superuser


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin) :

	def has_add_permission(self, request, obj=None) :

		return request.user.is_superuser

	def has_view_permission(self, request, obj=None) :
		
		return True

	def has_change_permission(self, request, obj=None) :
		
		return request.user.is_superuser

	def has_del_permission(self, request, obj=None) :
		
		return request.user.is_superuser