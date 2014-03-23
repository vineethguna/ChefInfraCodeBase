__author__ = 'vineeth'
import subprocess
import threading
import os
from app.models import NodeOnPremInfo
from app.constants import *
from app.validation import *


class ExecuteThread(threading.Thread):
    def __init__(self, node_name, ip_address, run_list, username, password):
        threading.Thread.__init__(self)
        self.node_name = node_name
        self.ip_address = ip_address
        self.run_list = run_list
        self.username = username
        self.password = password

    def execute_chef_script(self):
        shell_script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "app", "scripts",
                                         "onprem_bootstrap.sh")
        shell_parameters = "--node-name {0} --run-list {1} --ip-address {2} --username {3} --password {4}".format(
            self.node_name, self.run_list, self.ip_address, self.username, self.password
        )
        echo_command = "echo {0}".format(self.password)
        log_file = os.path.join(os.path.expanduser('~'), "logs", "onprem_log.log")
        shell_command = " ".format(echo_command, "|", shell_script_path, shell_parameters, "&>", log_file)
        output = subprocess.Popen(shell_command, shell=True)
        exit_code = output.returncode
        if exit_code == 0:
            NodeOnPremInfo.update_status(self.node_name, DEPLOY_SUCCESS)
        else:
            NodeOnPremInfo.update_status(self.node_name, DEPLOY_FAILURE)

    def run(self):
        self.execute_chef_script()


def start_deploy(node_name, ip_address, run_list, username, password):
    # Validate data
    if validate_onprem_data(node_name, ip_address, run_list, username, password):
        # Add db entry
        NodeOnPremInfo.add_deployment(node_name, ip_address, run_list, username, password)
        # Create a thread object to execute
        shell_thread = ExecuteThread(node_name, ip_address, run_list, username, password)
        shell_thread.start()
        return True
    else:
        return False