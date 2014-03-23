from django.db import models
from app.constants import *


# Create your models here.
class NodeOnPremInfo(models.Model):
    node_name = models.CharField(max_length=100, unique=True)
    ip_address = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=50)
    run_list = models.CharField(max_length=400)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    @staticmethod
    def get_deployments_info():
        return NodeOnPremInfo.objects.all()

    @staticmethod
    def add_deployment(node_name, ip_address, run_list, username, password):
        db_obj = NodeOnPremInfo(node_name=node_name, ip_address=ip_address, run_list=run_list, username=username,
                                password=password, status=PENDING_DEPLOY)
        db_obj.save()

    @staticmethod
    def update_status(node_name, status):
        NodeOnPremInfo.objects.filter(node_name=node_name).update(status=status)


class NodeOnCloudInfo(models.Model):
    node_name = models.CharField(max_length=100, unique=True)
    instance_type = models.CharField(max_length=100)
    cloud_provider = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    run_list = models.CharField(max_length=400)
    access_key = models.CharField(max_length=100, unique=True)
    secret_key = models.CharField(max_length=100, unique=True)

    @staticmethod
    def get_deployments_info():
        return NodeOnCloudInfo.objects.all()

    @staticmethod
    def add_deployment(node_name, access_key, secret_key, run_list, instance_type):
        db_obj = NodeOnCloudInfo(node_name=node_name, instance_type=instance_type, run_list=run_list, access_key=access_key,
                             secret_key=secret_key, cloud_provider='aws', status=PENDING_DEPLOY)
        db_obj.save()

    @staticmethod
    def update_status(node_name, status):
        NodeOnCloudInfo.objects.filter(node_name=node_name).update(status=status)