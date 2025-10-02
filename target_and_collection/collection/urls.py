from django.urls import path
from . import views

app_name = 'collection'

urlpatterns = [
    path('', views.index, name='index'),
    path('collections/', views.collection_list, name='collection_list'),
    path('collections/create/', views.collection_create, name='collection_create'),
    path('collections/<int:pk>/update/', views.collection_update, name='collection_update'),
    path('collections/<int:pk>/delete/', views.collection_delete, name='collection_delete'),
]