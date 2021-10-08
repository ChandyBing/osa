import requests
from apscheduler.schedulers.background import BackgroundScheduler
from osa_observation.failure_serializers import failureSerializer
from osa_observation.models import failure


# 请求报头
def header():
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/94.0.4606.61 Safari/537.36 '
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
    all_data = request_data('天眼接口')
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
    f = failure.objects.get(id=f_id)
    update_data = {
        'affected_customer': a_c,
        'affected_orders': a_o,
        'affected_amount': a_a,
        'state': 1
    }
    fs = failureSerializer(instance=f, data=update_data)
    fs.is_valid(raise_exception=True)
    fs.save()
