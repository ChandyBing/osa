from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.incomplete_failure_list, name='list')
]