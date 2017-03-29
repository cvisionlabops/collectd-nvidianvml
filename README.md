# collectd-nvidianvml
Collectd plugin for nvidia gpu's based on python and nvidia-ml-py python module

Install
```
sudo pip install collectd-nvidianvml
```

Create a config file `nvidianvml.conf` in `/etc/collect.d/`.

```
<LoadPlugin python>
  # Unlike most other LoadPlugin lines, this one should be a block containing the line "Globals true"
  # Because it is python plugin
  # `man 5 collectd-python`
  Globals true
</LoadPlugin>

<Plugin python>
  ModulePath "/usr/local/lib/python2.7/dist-packages/collectd-nvidianvml/"

  # To output python traces in syslog, set 'true'
  LogTraces true

  Import "nvidianvml"
  <Module nvidianvml>
    Verbose true
  </Module>

</Plugin>
```

### Note about debug collectd modules.

On ubuntu I'am faced with problem: collectd doesn't log python module errors (python errors) to syslog.

Solution

```
service collectd stop

# See errors, fix it.
collectd -f -C /etc/collectd.conf

# And start collect again
service collectd start
```

### Pipy

> http://peterdowns.com/posts/first-time-with-pypi.html

Do it once with new package:

```bash
python setup.py register -r pypi
```

To upload a new version you should run this (build and upload):

```bash
python setup.py sdist upload -r pypi
```
