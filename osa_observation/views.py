# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_list_or_404
from osa_observation.get_data import *
from osa_observation.models import failure
from osa_observation.failure_serializers import failureSerializer


def insert():
    data = {'序号': 1,
            'failure_system_name': 'aah',
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


def store_data(request):
    store_from_tianyan()
    try:
        f = failure.objects.all()
        response = {'msg': 1, 'status': 'success'}
    except f.DoesNotExist:
        response = {'msg': 0, 'status': 'failed'}
    return HttpResponse(response)


def complete_failure_list(request):
    all_data = get_list_or_404(failure, state=1)
    fs = failureSerializer(instance=all_data)
    response = {'msg': 1, 'status': 'success', 'data': fs.data}
    return HttpResponse(response)


def system_failure_list(request, request_id):
    system_dict = {
        '0': '订单中心', '1': '创新头条',
        '2': '活动中心', '3': '联通APP',
        '4': '汇聚中心', '5': '产商品中心',
        '6': '数据中台', '7': '新客服'
    }
    system_name = system_dict.get(str(request_id))
    system_data = get_list_or_404(failure, state=1, failure_system_name=system_name)
    fs = failureSerializer(instance=system_data)
    response = {'msg': 1, 'status': 'success', 'data': fs.data}
    return HttpResponse(response)


def incomplete_failure_list(request):
    all_data = get_list_or_404(failure, state=0)
    fs = failureSerializer(instance=all_data)
    data = {
        'id': fs.data.get('id'), 'failure_system_name': fs.data.get('failure_system_name'),
        'failure_happen_time': fs.data.get('failure_happen_time'), 'failure_impact': fs.data.get('failure_impact'),
        'failure_level': fs.data.get('failure_level')
    }
    response = {'msg': 1, 'status': 'success', 'data': data}
    return HttpResponse(response)


def add_data(request, request_id):
    a_c = request.POST('a_c')
    a_o = request.POST('a_o')
    a_a = request.POST('a_a')
    store_from_form(request_id, a_c, a_o, a_a)
    response = {'msg': 1, 'status': 'success'}
    return HttpResponse(response)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
