import pytest
import pdb
from cvp_checks import utils
import threading
nodes_without_ens3 = []


class MyThread (threading.Thread):
    def __init__(self, node, ens3_interfaces):
        threading.Thread.__init__(self)
        self.node = node
        self.ens3_interfaces = ens3_interfaces

    def run(self):
        print("Starting")
        check_interfaces(self.node, self.ens3_interfaces)


def test_check_ens3_interfaces(local_salt_client):
    active_nodes = utils.get_active_nodes()
    ens3_interfaces = local_salt_client.cmd(
        "L@"+','.join(active_nodes), 'cmd.run', ['ifconfig ens3'], expr_form='compound')
    nodes = ens3_interfaces.keys()
    for node in nodes:
        thread = MyThread(node, ens3_interfaces)
        thread.setName(node)
        thread.start()
    assert len(nodes_without_ens3) == 0, "Node is not contain ens3 interface: ".format(nodes_without_ens3)


def check_interfaces(node, ens3_interfaces):
        if "Device not found" in ens3_interfaces[node]:
            nodes_without_ens3.append(node)
            