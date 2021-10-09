from django.urls import path

from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('CompleteList/', views.complete_failure_list, name='CompleteList'),
    path('CompleteList/<int:request_id>/', views.system_failure_list, name='SystemList'),
    path('IncompleteList/', views.incomplete_failure_list, name='IncompleteList'),
    path('IncompleteList/<int:request_id>/', views.single_failure, name='SingleFailure'),
]