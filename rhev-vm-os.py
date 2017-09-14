#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2017 Javier Bahillo <jbahillo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import print_function
from ovirtsdk.api import API
from getpass import getpass
import sys


def get_cluster_name(id):
    for cluster in clusters:
        if cluster.id == id:
            return cluster.name
    return ""


hostname = "RHEV-MANAGER"
username = "admin@internal"
password = getpass("Password para usuario RHEV {u}: ".format(u=username))

try:
    api = API(url="https://%s:443" % hostname,
              username=username,
              password=password,
              ca_file="ca.pem",
              insecure=True)
    print("Connected to %s successfully!" % api.get_product_info().name)
    vms = api.vms.list(max=3000)
    hosts = api.hosts.list(max=100)
    clusters = api.clusters.list(max=100)
    api.disconnect()
except Exception as ex:
    print("Unexpected error: %s" % ex)
    sys.exit(1)

vms_content = "Name;Cluster name;CPU cores;Memory (bytes);Status;Template ID\n"
hosts_content = "Name;Cluster name;Address;CPU cores;Memory (bytes)\n"

for vm in vms:
    vms_content += vm.name + ";" + get_cluster_name(vm.cluster.id) + ";" + str(vm.cpu.topology.cores) + ";" \
                   + str(vm.memory) + ";" + vm.status.state + ";" + vm.template.id + ";" + str(vm.os.get_type()) + ";" +"\n"


with open("vms_os.csv", "w") as vms_file:
    vms_file.write(vms_content)
