import requests
from apscheduler.schedulers.blocking import BlockingScheduler


def job():
    print('job')


# 设置定期任务
def store_on_schedule():
    schedule = BlockingScheduler()
    schedule.add_job(job, 'interval', hours=1)
    schedule.start()


def dirt_test():
    dirt = {'0': '订单系统', '运保中心': 1}
    print(dirt.get('0'))


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


if __name__ == '__main__':
    dirt_test()
