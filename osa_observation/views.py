from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from osa_observation.get_data import store_from_form

from osa_observation.failure_serializers import failureSerializer


def insert():
    data = {'序号': 1,
            'failure_system_name': 'aaaaaa',
            'failure_happen_time': '2021-09-30 02:35:00.000000',
            'failure_recover_time': '2021-09-30 02:35:00.000000',
            'keep_time': '0',
            'failure_scope_batch_id': '2',
            'failure_impact': '2',
            'failure_level': '2',
            'measure_completion_status': '2'
            }
    s = failureSerializer(data=data)
    s.is_valid(raise_exception=True)
    s.save()


def get_form(request):
    f_id = request.POST('f_id')
    a_c = request.POST('a_c')
    a_o = request.POST('a_o')
    a_a = request.POST('a_a')
    store_from_form(f_id, a_c, a_o, a_a)
    response = {'msg': 1, 'status': 'success'}
    return HttpResponse(response)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


if __name__=='__main__':
