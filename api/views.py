# Create your views here.
import json
from urllib.request import Request
from rest_framework import viewsets
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from api.get_data import *
from api.models import failure
from api.serializers import failureSerializer


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


def add_info_test(request, failure_id):
    url = 'http://127.0.0.1:8000/api/partlist/failure_id=' + str(failure_id)
    return render(request, 'api/submit.html', request_data(url))


class FailueList(viewsets.ModelViewSet):
    queryset = failure.objects.all()
    serializer_class = failureSerializer

    def failure_list_all(self, request: Request, pagenum, pagesize, query='', system_name=''):
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
        querys = queryset.filter(state=1, failure_impact__contains=query,
                                 failure_system_name__contains=system_name).values('id', 'failure_system_name',
                                                                                   'failure_happen_time',
                                                                                   'failure_impact',
                                                                                   'failure_level',
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

    def failure_list_part(self, request: Request, pagenum, pagesize, query='', system_name=''):
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
        querys = queryset.filter(state=0, failure_impact__contains=query,
                                 failure_system_name__contains=system_name).values('id',
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

        # 查询数据库
        queryset = self.filter_queryset(self.get_queryset())
        query = queryset.filter(id=failure_id, state=0).values('id', 'failure_system_name', 'failure_happen_time'
                                                               , 'failure_impact', 'failure_level')

        # 序列化查询结果并response
        response_data = failureSerializer(instance=query, many=True).data
        response = {'failureList': response_data}
        return HttpResponse(json.dumps(response, ensure_ascii=False))

    def failure_info_add(self, request: Request, failure_id):
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
            a_c = request.POST['ac']
            a_o = request.POST['ao']
            a_a = request.POST['aa']

            # 将填写的数据存入库中并返回填写状态
            if store_from_form(failure_id, a_c, a_o, a_a):
                response = {'msg': 'success', 'status': 1}
            else:
                response = {'msg': 'failed', 'status': 0}
            return HttpResponse(json.dumps(response, ensure_ascii=False))
