# Create your views here.
import json
from encodings import gbk
from urllib.request import Request
from django.http import HttpResponse

from rest_framework import viewsets
from django.core.paginator import Paginator
from api.get_data import *
from api.models import failure
from api.serializers import failureSerializer
from api.response import *


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


class FailueList(viewsets.ModelViewSet):
    queryset = failure.objects.all()
    serializer_class = failureSerializer

    def failure_list_all(self, request: Request, pagenum, pagesize, query=None):
        """
            获取所有系统已填写故障数据

            入参:
                request: 请求
                pagenum: 当前页码
                pagesize: 单页条数
                query: 故障现象（可选）

            返回:
                total: 总页码
                pagenum: 当前页码
                failureList: 故障列表

        """
        # 查询数据库
        queryset = self.filter_queryset(self.get_queryset())
        if query is None:
            querys = queryset.filter(state=1).values('id', 'failure_system_name', 'failure_happen_time',
                                                     'failure_impact', 'failure_level', 'affected_customer',
                                                     'affected_orders', 'affected_amount')
        else:
            querys = queryset.filter(state=1, failure_impact__contains=query).values('id', 'failure_system_name',
                                                                                     'failure_happen_time',
                                                                                     'failure_impact', 'failure_level',
                                                                                     'affected_customer',
                                                                                     'affected_orders',
                                                                                     'affected_amount')

        # 将查询结果根据页码参数分页
        paginator = Paginator(querys, pagesize)
        page_obj = paginator.get_page(pagenum)
        pagecount = paginator.num_pages

        # 序列化查询结果并response
        response_data = failureSerializer(instance=page_obj, many=True).data
        response = {'total': pagecount, 'pagenum': pagenum, 'failureList': response_data}
        return HttpResponse(json.dumps(response, ensure_ascii=False))

    def failure_list_system(self, request: Request, system_name, pagenum, pagesize):
        """
            获取指定系统已填写故障数据

            入参:
                request: 请求
                system_name: 故障所属系统名
                pagenum: 当前页码
                pagesize: 单页条数

            返回:
                total: 总页码
                pagenum: 当前页码
                failureList: 故障列表
        """

        # 根据system_name查询数据库
        queryset = self.filter_queryset(self.get_queryset())
        query = queryset.filter(state=1, failure_system_name__contains=system_name).values('id', 'failure_system_name',
                                                                                           'failure_happen_time',
                                                                                           'failure_impact',
                                                                                           'failure_level',
                                                                                           'affected_customer',
                                                                                           'affected_orders',
                                                                                           'affected_amount')

        # 将查询结果根据页码参数分页
        paginator = Paginator(query, pagesize)
        page_obj = paginator.get_page(pagenum)
        pagecount = paginator.num_pages

        # 序列化查询结果并response
        response_data = failureSerializer(instance=page_obj, many=True).data
        response = {'total': pagecount, 'pagenum': pagenum, 'failureList': response_data}
        return HttpResponse(json.dumps(response, ensure_ascii=False))

    def failure_list_part(self, request: Request, pagenum, pagesize, query=None):
        """
            获取所有系统待填写故障数据

            入参:
                request: 请求
                pagenum: 当前页码
                pagesize: 单页条数
                query: 故障现象（可选）

            返回:
                total: 总页码
                pagenum: 当前页码
                failureList: 故障列表
        """

        # 查询数据库
        queryset = self.filter_queryset(self.get_queryset())
        if query is None:
            querys = queryset.filter(state=0).values('id', 'failure_system_name', 'failure_happen_time',
                                                     'failure_impact', 'failure_level')
        else:
            querys = queryset.filter(state=0, failure_impact__contains=query).values('id',
                                                                                     'failure_system_name',
                                                                                     'failure_happen_time',
                                                                                     'failure_impact',
                                                                                     'failure_level')

        # 将查询结果根据页码参数分页
        paginator = Paginator(querys, pagesize)
        page_obj = paginator.get_page(pagenum)
        pagecount = paginator.num_pages

        # 序列化查询结果并response
        response_data = failureSerializer(instance=page_obj, many=True).data
        response = {'total': pagecount, 'pagenum': pagenum, 'failureList': response_data}
        return HttpResponse(json.dumps(response, ensure_ascii=False))

    def failure_list_one(self, request: Request, failure_id):
        """
            获取单个待填写故障数据

            入参:
                request: 请求
                failure_id: 故障唯一标识

            返回:
                failureList: 响应数据
        """
        # 获取参数
        # failure_id = int(request.GET.get('failure_id'))

        # 查询数据库
        queryset = self.filter_queryset(self.get_queryset())
        query = queryset.filter(id=failure_id, state=0).values('id', 'failure_system_name', 'failure_happen_time'
                                                               , 'failure_impact', 'failure_level')

        # 序列化查询结果并response
        response_data = failureSerializer(instance=query, many=True).data
        response = {'failureList': response_data}
        return HttpResponse(json.dumps(response, ensure_ascii=False))

    def failure_info_add(self, request: Request):
        """
            将获取的表单数据存入数据库

            入参:
                request: 请求
                failure_id: 故障唯一标识

            返回: msg: 响应成功/失败信息
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
            return HttpResponse(json.dumps(response, ensure_ascii=False))
