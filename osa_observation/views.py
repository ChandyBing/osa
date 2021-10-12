# Create your views here.
import json
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from django.core.paginator import Paginator
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


# 获取天眼全量数据并入库
def store_data1(request):
    store_from_tianyan()
    try:
        f = failure.objects.all()
        response = {'msg': 'success', 'status': 1}
    except f.DoesNotExist:
        response = {'msg': 'failed', 'status': 0}
    return HttpResponse(json.dumps(response))


# 获取天眼增量数据并入库
def store_data2(request):
    store_on_schedule()
    try:
        f = failure.objects.all()
        response = {'msg': 'success', 'status': 1}
    except f.DoesNotExist:
        response = {'msg': 'failed', 'status': 0}
    return HttpResponse(json.dumps(response))


def failure_list_all(request):
    """
        获取所有系统已写故障数据
        :param request: 请求
        :param pagenum: 当前页码
        :param pagesize: 单页条数
        :return: code: 响应码
                 data: 响应数据
    """
    # 获取参数
    pagenum = int(request.GET.get('pagenum'))
    pagesize = int(request.GET.get('pagesize'))

    # 查询数据库
    query = failure.objects.filter(state=1).values()

    # 将查询结果根据页码参数分页
    paginator = Paginator(query, pagesize)
    page_obj = paginator.get_page(pagenum)

    # 序列化查询结果并response
    response_data = failureSerializer(instance=page_obj, many=True).data
    response = {'code': 200, 'data': response_data}
    return HttpResponse(json.dumps(response))


def failure_list_system(request):
    """
       获取单个系统已填写故障数据
       :param request: 请求
       :param system_id: 故障所属系统id
       :param pagenum: 当前页码
       :param pagesize: 单页条数
       :return: code: 响应码
                data: 响应数据
    """
    # 获取参数
    system_id = request.GET.get('system_id')
    pagenum = int(request.GET.get('pagenum'))
    pagesize = int(request.GET.get('pagesize'))

    # system_id映射表
    system_dict = {
        '0': '订单中心', '1': '创新头条',
        '2': '活动中心', '3': '联通APP',
        '4': '汇聚中心', '5': '产商品中心',
        '6': '数据中台', '7': '新客服', '8': '集中-cBSS'
    }

    # 根据system_id查询数据库
    system_name = system_dict[(str(system_id))]
    query = failure.objects.filter(state=1, failure_system_name=system_name)

    # 将查询结果根据页码参数分页
    paginator = Paginator(query, pagesize)
    page_obj = paginator.get_page(pagenum)

    # 序列化查询结果并response
    response_data = failureSerializer(instance=page_obj, many=True).data
    response = {'code': 200, 'data': response_data}
    return HttpResponse(json.dumps(response))


def failure_list_part(request):
    """
        获取所有系统待填写故障数据
        :param request: 请求
        :param pagenum: 当前页码
        :param pagesize: 单页条数
        :return: code: 响应码
                 data: 响应数据
    """
    # 获取参数
    pagenum = int(request.GET.get('pagenum'))
    pagesize = int(request.GET.get('pagesize'))

    # 查询数据库
    query = failure.objects.filter(state=0).values('id')

    # 将查询结果根据页码参数分页
    paginator = Paginator(query, pagesize)
    page_obj = paginator.get_page(pagenum)

    # 序列化查询结果并response
    response_data = failureSerializer(instance=page_obj, many=True).data
    response = {'code': 200, 'data': response_data}
    return HttpResponse(json.dumps(response))


def failure_list_one(request):
    """
        获取单个待填写故障数据
        :param request: 请求
        :param failure_id: 故障标识
        :return: code: 响应码
                 data: 响应数据
    """
    # 获取参数
    failure_id = int(request.GET.get('failure_id'))

    # 查询数据库
    query = failure.objects.filter(id=failure_id, state=0).values('id', 'failure_system_name', 'failure_happen_time',
                                                                  'failure_impact', 'failure_level')

    # 序列化查询结果并response
    response_data = failureSerializer(instance=query, many=True).data
    response = {'code': 200, 'data': response_data}
    return HttpResponse(json.dumps(response))


def failure_info_add(request):
    """
        获取单个待填写故障数据
        :param request: 请求
        :param failure_id: 故障标识
        :return: msg: 响应成功/失败信息
                 status: 响应成功/失败状态
    """
    if request.method == 'POST':
        # 获取表单传入的参数
        failure_id = int(request.POST.get('failure_id'))
        a_c = request.POST['a_c']
        a_o = request.POST['a_o']
        a_a = request.POST['a_a']

        # 将填写的数据存入库中并返回填写状态
        if store_from_form(failure_id, a_c, a_o, a_a):
            response = {'msg': 'success', 'status': 1}
        else:
            response = {'msg': 'failed', 'status': 0}
        return HttpResponse(json.dumps(response))


def index(request):
    return render(request, 'osa_observation/index.html')


class APIInfoViewSet(viewsets.ModelViewSet):
    """
    简介
    """
    queryset = failure.objects.all()
    serializer_class = failureSerializer

    def get(self):
        pass

    def post(self):
        pass
