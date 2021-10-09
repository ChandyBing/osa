# Create your views here.
import json
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, render
from osa_observation.get_data import *
from osa_observation.models import failure
from osa_observation.failure_serializers import failureSerializer


def insert():
    datas = [{
            'failure_system_name': '集中-cBSS',
            'failure_happen_time': '2021-07-01 07:35:00',
            'failure_recover_time': '2021-07-01 07:37:00',
            'keep_time': '2',
            'failure_scope_batch_id': '北京,江苏,福建,云南,黑龙江,浙江,天津,上海,甘肃,广东,四川,广西,西藏,辽宁,湖南,新疆,江西',
            'failure_impact': '73.1meta节点宕库，影响新架构1-4域计费批价延迟，账管查缴办部分失败，信控停开机延迟',
            'failure_level': '一般故障',
            'measure_completion_status': '1/1'
            }, {
            'failure_system_name': '辽宁-电子发票系统',
            'failure_happen_time': '2021-07-02 09:50:00',
            'failure_recover_time': '2021-07-02 10:06:00',
            'keep_time': '16',
            'failure_scope_batch_id': '辽宁',
            'failure_impact': '影响辽宁省分开具电子普通发票',
            'failure_level': '一般故障',
            'measure_completion_status': '2/2'
            }, {
            'failure_system_name': '集中-智慧客服',
            'failure_happen_time': '2021-07-03 09:21:00',
            'failure_recover_time': '2021-07-03 09:28:00',
            'keep_time': '7',
            'failure_scope_batch_id': '内蒙古,北京,山东,河北,山西,浙江,青海,湖北,西藏,四川,重庆,贵州,甘肃,宁夏,新疆,黑龙江',
            'failure_impact': '10010呼入提示繁忙，提示稍后再拨',
            'failure_level': '一般故障',
            'measure_completion_status': '2/2'
            }, {
            'failure_system_name': '黑龙江-省分接口',
            'failure_happen_time': '2021-07-03 18:00:00',
            'failure_recover_time': '2021-07-03 18:13:00',
            'keep_time': '13',
            'failure_scope_batch_id': '黑龙江',
            'failure_impact': '携号转网用户',
            'failure_level': '一般故障',
            'measure_completion_status': '0/0'
            }, {
            'failure_system_name': '山西-云网短信平台',
            'failure_happen_time': '2021-07-06 15:00:00',
            'failure_recover_time': '2021-07-06 16:00:00',
            'keep_time': '60',
            'failure_scope_batch_id': '山西',
            'failure_impact': '携转用户收不到携转授权码，无法查询携出资格..',
            'failure_level': '待定级',
            'measure_completion_status': '1/1'
            }]
    for data in datas:
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
    return HttpResponse(json.dumps(response))


def complete_failure_list(request):
    query = get_list_or_404(failure, state=1)
    response_data = failureSerializer(instance=query, many=True).data
    response = {'msg': 1, 'status': 'success', 'data': response_data}
    return HttpResponse(json.dumps(response))


def system_failure_list(request, request_id):
    system_dict = {
        '0': '订单中心', '1': '创新头条',
        '2': '活动中心', '3': '联通APP',
        '4': '汇聚中心', '5': '产商品中心',
        '6': '数据中台', '7': '新客服', '8': '集中-cBSS'
    }
    system_name = system_dict[(str(request_id))]
    query = get_list_or_404(failure, state=1, failure_system_name=system_name)
    response_data = failureSerializer(instance=query, many=True).data
    response = {'msg': 1, 'status': 'success', 'data': response_data}
    return HttpResponse(json.dumps(response))


def incomplete_failure_list(request):
    query = get_list_or_404(failure, state=0)
    data_list = failureSerializer(instance=query, many=True).data
    response_data = []
    for raw_data in data_list:
        shuffled_data = {
            'id': raw_data['id'], 'failure_system_name': raw_data['failure_system_name'],
        }
        response_data.append(shuffled_data)
    response = {'msg': 1, 'status': 'success', 'data': response_data}
    return HttpResponse(json.dumps(response))


def single_failure(request, request_id):
    query = get_list_or_404(failure, id=request_id, state=0)
    data_list = failureSerializer(instance=query, many=True).data
    response_data = {
        'id': data_list[0]['id'], 'failure_system_name': data_list[0]['failure_system_name'],
    }
    response = {'msg': 1, 'status': 'success', 'request_id': request_id,'data': response_data}
    return render(request, 'osa_observation/submit.html', response)


def add_data(request, request_id):
    a_c = request.POST['a_c']
    a_o = request.POST['a_o']
    a_a = request.POST['a_a']
    store_from_form(request_id, a_c, a_o, a_a)
    response = {'msg': 1, 'status': 'success'}
    return HttpResponse(json.dumps(response))


def index(request):
    return render(request, 'osa_observation/index.html')
