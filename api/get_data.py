import requests
from apscheduler.schedulers.background import BackgroundScheduler
from .serializers import failureSerializer
from .models import failure


# 请求报头
def header():
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/94.0.4606.81 Safari/537.36 '
    }
    return headers


# request请求json数据
def request_data(url):
    try:
        response = requests.get(url, headers=header(), verify=False)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        return None


# 获取全量数据
def store_from_tianyan():
    # 若数据库不为空，清空数据库
    if len(failure.objects.all()) > 0:
        failure.objects.all().delete()

    # 数据入库
    all_data = request_data('http://localhost:8000/osa_observation/CompleteList/8/')['data']
    for data in all_data:
        s = failureSerializer(data=data)
        s.is_valid(raise_exception=True)
        s.save()


# 接口获取数据
def store_on_schedule_job():
    new_data = request_data('天眼接口')
    old_ids = failure.objects.all()[0].id
    for data in new_data:
        if data.id in old_ids:
            f = failure.objects.get(id=data.id)
            fs = failureSerializer(instance=f, data=data)
            fs.is_valid(raise_exception=True)
            fs.save()
        else:
            s = failureSerializer(data=data)
            s.is_valid(raise_exception=True)
            s.save()


# 定时获取数据
def store_on_schedule():
    schedule = BackgroundScheduler()
    schedule.add_job(store_on_schedule_job, 'interval', hours=3)
    schedule.start()


# 获取表单数据
def store_from_form(f_id, a_c, a_o, a_a):
    f = failure.objects.filter(id=f_id)
    if len(f) == 1:
        update_data = {
            'affected_customer': a_c,
            'affected_orders': a_o,
            'affected_amount': a_a,
            'state': 1
        }
        fs = failureSerializer(instance=f.first(), data=update_data)
        fs.is_valid(raise_exception=True)
        fs.save()
        return True
    else:
        return False


def insert():
    dataset = [{
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
    }, {
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
    }, {
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
    for data in dataset:
        s = failureSerializer(data=data)
        s.is_valid(raise_exception=True)
        s.save()
