#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2017 Javier Bahillo <javier.bahillo@gmail.com>
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
from ovirtsdk.xml import params 
from getpass import getpass
import sys


def get_cluster_name(id):
    for cluster in clusters:
        if cluster.id == id:
            return cluster.name
    return ""

def get_storagedomain_name(id):
    for storagedomain in storagedomains:
        if storagedomain.id == id:
            return storagedomain.name
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
    storagedomains= api.storagedomains.list()
    vms = api.vms.list(max=3000)
    clusters = api.clusters.list(max=100)
except Exception as ex:
    print("Unexpected error: %s" % ex)
    sys.exit(1)

disks_content = "VM;Disk;Storage;Cluster\n"


for vm in vms:
     disks = vm.get_disks()
     for disk in disks.list():
         disk_name = disk.get_name()
         try:
             disk_sds = disk.storage_domains.storage_domain
         except:
             pass
         for sd in disk_sds:
             sd_id =  sd.get_id()
             disks_content += str(vm.name + ";" + disk_name  + ";" + get_storagedomain_name(sd_id) +  ";" + get_cluster_name(vm.cluster.id) + "\n")


with open("disks.csv", "w") as disk_file:
    disk_file.write(disks_content)
