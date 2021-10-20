from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('alllist/',
         views.FailueList.as_view({'get': 'failure_list_all'})),

    path('partlist/',
         views.FailueList.as_view({'get': 'failure_list_part'})),

    path('partlist/onefailure/', views.FailueList.as_view({'get': 'failure_list_one'})),

    path('partlist/addinfo/', views.FailueList.as_view({'post': 'failure_info_add'})),

    path('partlist/addtest/', views.add_info_test)
]
