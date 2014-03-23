__author__ = 'vineeth'
import subprocess
import threading
import os
from app.models import NodeOnCloudInfo
from app.constants import *
from app.validation import *


class ExecuteThread(threading.Thread):
    def __init__(self, node_name, access_key, secret_key, run_list, instance_type):
        threading.Thread.__init__(self)
        self.node_name = node_name
        self.access_key = access_key
        self.secret_key = secret_key
        self.run_list = run_list
        self.instance_type = instance_type

    def execute_chef_script(self):
        shell_script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "scripts",
                                         CLOUD_SCRIPT_NAME)
        shell_parameters = "--node-name {0} --run-list {1} --access-key {2} --secret-key {3} --instance-type {4}".\
            format(
                self.node_name, self.run_list, self.access_key, self.secret_key, self.instance_type
            )
        log_file = os.path.join(os.path.expanduser('~'), "logs", "cloud_log.log")
        shell_command = " ".format(shell_script_path, shell_parameters, "&>", log_file)
        output = subprocess.Popen(shell_command, shell=True)
        exit_code = output.returncode
        if exit_code == 0:
            NodeOnCloudInfo.update_status(self.node_name, DEPLOY_SUCCESS)
        else:
            NodeOnCloudInfo.update_status(self.node_name, DEPLOY_FAILURE)

    def run(self):
        self.execute_chef_script()


def start_deploy(node_name, access_key, secret_key, run_list, instance_type):
    # Validate data
    if validate_cloud_data(node_name, access_key, secret_key, run_list, instance_type):
        # Add db entry
        NodeOnCloudInfo.add_deployment(node_name, access_key, secret_key, run_list, instance_type)
        # Create a thread object to execute
        shell_thread = ExecuteThread(node_name, access_key, secret_key, run_list, instance_type)
        shell_thread.start()
        return True
    else:
        return False