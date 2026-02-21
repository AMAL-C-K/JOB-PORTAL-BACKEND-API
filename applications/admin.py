from django.contrib import admin
from .models import Application


admin.site.register(Application)

class ApplicationAdmin(admin.ModelAdmin):

    list_display = ('id','job','candidate','status','applied_at')
    list_filter = ('job__title','candidate__username')
    ordering = ('-applied_at',)
