from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from app.models import NodeOnCloudInfo, NodeOnPremInfo
from app.onprem.deploy import start_deploy as onprem_deploy
from app.cloud.deploy import start_deploy as cloud_deploy

# Create your views here.
def index(request):
    if request.method == 'GET':
        return render_to_response('index.html')
    else:
        pass


# View which handles onprem homepage
def on_prem_index(request):
    if request.method == 'GET':
        on_prem_entries = NodeOnPremInfo.get_deployments_info()
        return render_to_response('onprem_index.html')
    else:
        pass


# View which handles cloud homepage
def cloud_index(request):
    if request.method == 'GET':
        cloud_entries = NodeOnCloudInfo.get_deployments_info()
        return render_to_response('cloud_index.html')
    else:
        pass


# View which gives form for onprem deployments
def create_on_prem_deployment(request):
    if request.method == 'GET':
        return render_to_response('onprem_deploy.html')
    else:
        pass


# View which gives form for cloud deployment
def create_cloud_deployment(request):
    if request.method == 'GET':
        return render_to_response('cloud_deploy.html')
    else:
        pass


# View which handles on prem deployment
def handle_on_prem_deployment(request):
    if request.method == 'POST':
        node_name = request['POST']['node_name']
        ip_address = request['POST']['ip_address']
        username = request['POST']['username']
        password = request['POST']['password']
        run_list = request['POST']['run_list']
        result = onprem_deploy(node_name, ip_address, run_list, username, password)
        if result:
            render_to_response('onprem_index.html')
        else:
            pass
    else:
        pass


# View which handles cloud deployment
def handle_cloud_deployment(request):
    if request.method == 'POST':
        node_name = request['POST']['node_name']
        access_key = request['POST']['access_key']
        secret_key = request['POST']['secret_key']
        instance_type = request['POST']['instance_type']
        run_list = request['POST']['run_list']
        result = cloud_deploy(node_name, access_key, secret_key, run_list, instance_type)
        if result:
            render_to_response('cloud_index.html')
        else:
            pass
    else:
        pass
