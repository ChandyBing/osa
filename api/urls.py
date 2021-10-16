from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('alllist/pagenum=<int:pagenum>&&pagesize=<int:pagesize>', views.FailueList.as_view({'get': 'failure_list_all'})),
    path('alllist/pagenum=<int:pagenum>&&pagesize=<int:pagesize>&&query=<str:query>', views.FailueList.as_view({'get': 'failure_list_all'})),
    path('alllist/<str:system_name>/pagenum=<int:pagenum>&&pagesize=<int:pagesize>', views.FailueList.as_view({'get': 'failure_list_system'})),
    path('partlist/pagenum=<int:pagenum>&&pagesize=<int:pagesize>', views.FailueList.as_view({'get': 'failure_list_part'})),
    path('partlist/pagenum=<int:pagenum>&&pagesize=<int:pagesize>&&query=<str:query>', views.FailueList.as_view({'get': 'failure_list_part'})),
    path('partlist/failure_id=<int:failure_id>/', views.FailueList.as_view({'get': 'failure_list_one'})),
    path('partlist/submit/', views.FailueList.as_view({'post': 'failure_info_add'}))
]
