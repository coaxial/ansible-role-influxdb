import os

import testinfra.utils.ansible_runner
from distutils.version import LooseVersion

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_influxdb_service(host):
    s = host.service('influxdb')

    assert s.is_enabled
    assert s.is_running


def test_influxdb_package(host):
    p = host.package("influxdb")

    assert p.is_installed
    # 1.6.2 is the most recent version when writing this test
    assert LooseVersion(p.version) >= LooseVersion('1.6.2')


def test_config_file(host):
    f = host.file('/etc/influxdb/influxdb.conf')

    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o644


def test_config_dir(host):
    f = host.file('/etc/influxdb')

    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o755
