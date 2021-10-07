import requests
from osa_observation.failure_serializers import failureSerializer
from osa_observation.models import failure


def header():
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/94.0.4606.61 Safari/537.36 '
    }
    return headers


def request_data(url):
    try:
        response = requests.get(url, headers=header(), verify=False)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException:
        return None


def store_from_tianyan1():
    if len(failure.objects.all()) > 0:
        failure.objects.all().delete()
    all_data = request_data('天眼接口')
    for data in all_data:
        s = failureSerializer(data=data)
        s.is_valid(raise_exception=True)
        s.save()


def store_from_tianyan2():



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
