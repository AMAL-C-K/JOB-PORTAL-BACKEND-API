from django.contrib import admin
from .models import Job

admin.site.register(Job)

class JobAdmin(admin.ModelAdmin):
    list_display = ('id','title','employer','job_type','location','salary','created_at')
    list_filter = ('job_type','location','created_at')
    search_fields = ('title','employer__username')
    ordering = ('-created_at')