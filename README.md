influxdb
=========
  [![Build Status](https://travis-ci.org/coaxial/ansible-role-influxdb.svg?branch=master)](https://travis-ci.org/coaxial/ansible-role-influxdb)

Install and configure InfluxDB

Role Variables
--------------

Name | Default | Possible values | Description
---|---|---|---
`idb__admin_users` | unset | Array of users: `{username: 'admin', password: 'secret'}` **use encrypted vars** | Configure the admin user or users. Will be granted all privileges.
`idb__regular_users` | unset | Array of users: `{username: 'prometheus', password: 'secret'}` **use encrypted vars** | Configure the regular user or users.
`idb__databases` | unset | Array of databases: `{name: 'dbname', retention: '0s', user: [name: 'prometheus', privilege: 'ALL']}` | Configure the databases, their retention policy (for `autogen`), and their user permissions. `privilege` is one of `READ`, `WRITE`, `ALL`.

Note that some of the variables are inserted as is into influxQL queries. There
is potential for injecting commands this way. I chose not to mitigate this
because if you don't trust the people running playbooks and roles against your
infrastructure, then you have problems. And malicious users can run arbitrary
commands using the `shell` and `command` modules anyway if they really wanted
to do some damage; this is easier than injecting code in influxQL queries.

Every other setting is controlled by the `influxdb.conf` file in
`files/influxdb.conf`. The default file for this role is the one influxdb comes
with (c.f. https://docs.influxdata.com/influxdb/v1.6/administration/config/).
To use custom settings, place your own copy in `files/influxdb.conf`.


Example Playbook
----------------

```yaml
- hosts: all
  vars:
    idb__admin_users:
      - name: admin
        password: secret
    idb__regular_users:
      - name: jdoe
        password: hunter2
      - name: otheruser
        password: letmein
    idb__databases:
      - name: 'mydatabase'
        retention: '0s'  # optional, omitted if absent
        user:
          - name: jdoe
            privilege: ALL
          - name: otheruser
            privilege: READ
  roles:
    - coaxial.influxdb
```

License
-------

MIT

Author Information
------------------

Coaxial ([64b.it](https://64b.it))
