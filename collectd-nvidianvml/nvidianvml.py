#!/usr/bin/env python

# TODO
# Add info that this plugin does not require additional(custom) types defined.
# It uses default types from types.db

# Depends on
# pip install nvidia-ml-py

import collectd
from pynvml import *

VERBOSE_LOGGING = False
#VERBOSE_LOGGING = True

def log_verbose(msg):
    if not VERBOSE_LOGGING:
        return
    collectd.info('nvidianvml plugin [verbose]: %s' % msg)

def configure_callback(conf):
    global VERBOSE_LOGGING
    for c in conf.children:
        if c.key == 'Verbose':
            VERBOSE_LOGGING = bool(c.values[0])
        elif c.key == 'option':
            option == 'dummy'
        else:
            collectd.warning ('nvidianvml plugin: Unknown config key: %s.' % c.key)
    # Logging does not work at this stage.
    # Most likely the syslog plugin is not yet loaded
    #VERBOSE_LOGGING = True
    #log_verbose('Configured with option=%s' % (c.values))

def dispatch_value(plugin_instance, info, key, type, type_instance=None):
    if not type_instance:
        type_instance = key
    value = int(info)
    log_verbose('Sending value: %s=%s' % (type_instance, value))
    val = collectd.Values(plugin='nvidianvml')
    val.plugin_instance = plugin_instance
    val.type = type
    val.type_instance = type_instance
    val.values = [value]
    val.dispatch()

def read_callback():
    nvmlInit()
    deviceCount = nvmlDeviceGetCount()

    log_verbose('Read callback called')
    log_verbose('deviceCount is: %s' % (deviceCount)) 

    for i in range(deviceCount):
        handle = nvmlDeviceGetHandleByIndex(i)
        plugin_instance='nvidia%s' % (i)
        dispatch_value(plugin_instance, nvmlDeviceGetMemoryInfo(handle).total, 'total', 'memory')
        dispatch_value(plugin_instance, nvmlDeviceGetMemoryInfo(handle).used, 'used', 'memory')
        dispatch_value(plugin_instance, nvmlDeviceGetMemoryInfo(handle).total, 'free', 'memory')

        dispatch_value(plugin_instance, nvmlDeviceGetPowerUsage(handle), 'powerusage', 'power')
        dispatch_value(plugin_instance, nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU), 'temp', 'temperature')
        dispatch_value(plugin_instance, nvmlDeviceGetFanSpeed(handle), 'fanspeed', 'fanspeed')

        dispatch_value(plugin_instance, nvmlDeviceGetUtilizationRates(handle).gpu, 'util_gpu', 'percent')
        dispatch_value(plugin_instance, nvmlDeviceGetUtilizationRates(handle).memory, 'util_memory', 'percent')

collectd.register_config(configure_callback)
collectd.register_read(read_callback)
