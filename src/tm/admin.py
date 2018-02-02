from django.contrib import admin

from .models import Introducer, Template, Product, Applicant, Setting


class IntroducerAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'updated_at')
    list_display = ('name', 'auth_code', 'ip', 'is_active', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'is_active')
    ordering = ('name',)


class ProductAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'updated_at',)
    list_display = ('introducer', 'amount', 'term', 'is_active', 'updated_at')
    list_filter = ('introducer', 'amount', 'term', 'is_active')
    ordering = ('introducer', 'amount', 'term')


class ApplicantAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'updated_at')
    list_display = ('introducer', 'first_name', 'last_name', 'email', 'updated_at')
    list_filter = ('introducer',)
    ordering = ('introducer', 'first_name', 'last_name')


class SettingAdmin(admin.ModelAdmin):
    exclude = ('updated_at',)
    list_display = ('key', 'name', 'type', 'value', 'updated_at')
    ordering = ('name',)


admin.site.register(Introducer, IntroducerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(Setting, SettingAdmin)
