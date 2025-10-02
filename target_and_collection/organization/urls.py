from django.urls import path
from . import views

app_name = 'organization'

urlpatterns = [
    path('departments/', views.department_list, name='department_list'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/<int:pk>/update/', views.department_update, name='department_update'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),

    path('subdepartments/', views.subdepartment_list, name='subdepartment_list'),
    path('subdepartments/create/', views.subdepartment_create, name='subdepartment_create'),
    path('subdepartments/<int:pk>/update/', views.subdepartment_update, name='subdepartment_update'),
    path('subdepartments/<int:pk>/delete/', views.subdepartment_delete, name='subdepartment_delete'),

    path('rules/', views.rule_list, name='rule_list'),
    path('rules/create/', views.rule_create, name='rule_create'),
    path('rules/<int:pk>/update/', views.rule_update, name='rule_update'),
    path('rules/<int:pk>/delete/', views.rule_delete, name='rule_delete'),
    path('api/get_model_fields/', views.get_model_fields, name='get_model_fields'),
]