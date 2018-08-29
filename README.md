influxdb
=========
  [![Build Status](https://travis-ci.org/coaxial/ansible-role-influxdb.svg?branch=master)](https://travis-ci.org/coaxial/ansible-role-influxdb)

Install and configure InfluxDB

Role Variables
--------------

No variables to configure. Every setting is controlled by the `influxdb.conf` file in `files/influxdb.conf`. The default file is the one influxdb comes with (c.f. https://docs.influxdata.com/influxdb/v1.6/administration/config/). To use custom settings, place your own copy in `files/influxdb.conf`.


Example Playbook
----------------

```yaml
- hosts: all
  roles:
    - coaxial.influxdb
```

License
-------

MIT

Author Information
------------------

Coaxial ([64b.it](https://64b.it))
