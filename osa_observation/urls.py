from django.urls import path

from . import views
app_name = 'osa_observation'
urlpatterns = [
    path('', views.index, name='index'),
    path('alllist/', views.failure_list_all, name='alllist'),
    path('alllist/system/', views.failure_list_system, name='alllist_system'),
    path('partlist/', views.failure_list_part, name='partlist'),
    path('partlist/single/', views.failure_list_one, name='partlist_one'),
    path('partlist/submit/', views.failure_info_add, name='add_info')
]