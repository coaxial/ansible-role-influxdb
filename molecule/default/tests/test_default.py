import os
import re

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


def test_db_creation(host):
    # The first three lines are headers
    dblist = host.check_output('influx -execute "SHOW DATABASES" | sed 1,3d')

    assert 'testdb' in dblist


def test_users_creation(host):
    userlist = host.check_output('influx -execute "SHOW USERS" | sed 1,2d')

    assert re.compile(r'admin\s+true').search(userlist)
    assert re.compile(r'jdoe\s+false').search(userlist)
    assert re.compile(r'otheruser\s+false').search(userlist)


def test_retention(host):
    ret = host.check_output('influx -execute "SHOW RETENTION POLICIES ON'
                            ' testdb" | sed 1,2d')

    assert re.compile(r'autogen\s+336h0m0s').search(ret)


def test_db_grants(host):
    jdoegrants = host.check_output(
        'influx -execute "SHOW GRANTS FOR jdoe" | sed 1,2d')
    otherusergrants = host.check_output(
        'influx -execute "SHOW GRANTS FOR otheruser" | sed 1,2d')

    assert re.compile(r'testdb\s+ALL PRIVILEGES').search(jdoegrants)
    assert re.compile(r'testdb\s+READ').search(otherusergrants)
