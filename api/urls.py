from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('alllist/pagenum=<int:pagenum>&pagesize=<int:pagesize>/',
         views.FailueList.as_view({'get': 'failure_list_all'})),

    path('alllist/query=<str:query>/pagenum=<int:pagenum>&pagesize=<int:pagesize>/',
         views.FailueList.as_view({'get': 'failure_list_all'})),

    path('alllist/system_name=<str:system_name>/pagenum=<int:pagenum>&pagesize=<int:pagesize>/',
         views.FailueList.as_view({'get': 'failure_list_all'})),

    path('alllist/system_name=<str:system_name>/query=<str:query>/pagenum=<int:pagenum>&pagesize=<int:pagesize>/',
         views.FailueList.as_view({'get': 'failure_list_all'})),

    path('partlist/pagenum=<int:pagenum>&pagesize=<int:pagesize>/',
         views.FailueList.as_view({'get': 'failure_list_part'})),

    path('partlist/query=<str:query>/pagenum=<int:pagenum>&pagesize=<int:pagesize>/',
         views.FailueList.as_view({'get': 'failure_list_part'})),

    path('partlist/system_name=<str:system_name>/pagenum=<int:pagenum>&pagesize=<int:pagesize>/',
         views.FailueList.as_view({'get': 'failure_list_part'})),

    path('partlist/system_name=<str:system_name>/query=<str:query>/pagenum=<int:pagenum>&pagesize=<int:pagesize>/',
         views.FailueList.as_view({'get': 'failure_list_part'})),

    path('partlist/failure_id=<int:failure_id>/', views.FailueList.as_view({'get': 'failure_list_one'})),

    path('partlist/addinfo/<int:failure_id>/', views.FailueList.as_view({'post': 'failure_info_add'})),

    path('partlist/addtest/<int:failure_id>', views.add_info_test)
]
