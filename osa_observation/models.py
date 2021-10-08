from django.db import models

# Create your models here.
from django.db import models


class failure(models.Model):
    id = models.AutoField('序号', primary_key=True)
    failure_system_name = models.CharField('所属系统', max_length=255, default=None)
    failure_happen_time = models.DateTimeField('开始时间')
    failure_recover_time = models.DateTimeField('结束时间')
    keep_time = models.CharField('持续时间', max_length=255, default=None)
    failure_scope_batch_id = models.CharField('影响范围', max_length=255, default=None)
    failure_impact = models.TextField('故障现象', max_length=255, default=None)
    failure_level = models.CharField('故障等级', max_length=255, default=None)
    measure_completion_status = models.CharField('整改进度', max_length=255, default=None)
    affected_customer = models.CharField('影响人数', max_length=255)
    affected_orders = models.CharField('影响单量', max_length=255)
    affected_amount = models.CharField('影响金额', max_length=255)
    state = models.IntegerField('填写状态', default=0)
