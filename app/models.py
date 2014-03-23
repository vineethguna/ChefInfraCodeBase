from django.db import models

# Create your models here.
class NodeOnPremInfo(models.Model):
    hostname = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    run_list = models.CharField(max_length=400)

class NodeOnCloud(models.Model):
    hostname = models.CharField(max_length=100)
    instance_type = models.CharField(max_length=100)
    cloud_provider = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    run_list = models.CharField(max_length=400)