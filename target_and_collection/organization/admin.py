from django.contrib import admin
from .models import Department, SubDepartment, Rule, Condition, RuleTarget

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(SubDepartment)
class SubDepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    list_filter = ('department',)
    search_fields = ('name',)

class ConditionInline(admin.StackedInline):
    model = Condition
    extra = 1

class RuleTargetInline(admin.StackedInline):
    model = RuleTarget
    extra = 1

@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    inlines = [ConditionInline, RuleTargetInline]

# Register your models here.
