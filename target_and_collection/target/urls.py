from django.urls import path
from . import views

app_name = 'target'

urlpatterns = [
    path('targets/', views.target_list, name='target_list'),
    path('targets/create/', views.target_create, name='target_create'),
    path('targets/<int:pk>/update/', views.target_update, name='target_update'),
    path('targets/<int:pk>/delete/', views.target_delete, name='target_delete'),
]