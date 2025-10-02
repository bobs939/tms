from django.contrib import admin
from .models import Target

@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'sub_department', 'value')
    list_filter = ('department', 'sub_department')
    search_fields = ('name', 'description')

# Register your models here.
