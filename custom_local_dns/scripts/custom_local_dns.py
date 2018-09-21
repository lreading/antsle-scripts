#! /usr/bin/env python2
''' 
Derived from Antsle's work at https://github.com/antsle/antsleOS/blob/c25d5f407a7921c72ceff479db7ce78159941481/usr/local/bin/antletsld

Register mDNS/DNS-SD alias names for your computer using the Avahi daemon

This script will register an alternate CNAME alias besides your hostname,
which could be useful for ex. when serving several http virtual hosts to 
your friends on the local network and you don't want to make them configure
their /etc/hosts.

Why a CNAME? You could also publish your current address with avahi-publish-address
but on a multihomed host (connected via wifi0 and eth0 perhaps) a single
address will not be valid on both networks. So this publishes a CNAME to your
hostname, which, by default, is already published by Avahi.

Aliases will be added for antlet10.local through antlet254.local. This will enable
you to access antlets via the browser without any DNS configuration.

The aliases will stay published until the script runs.
'''
import avahi, dbus, os
from encodings.idna import ToASCII

TTL = 60
# Got these from /usr/include/avahi-common/defs.h
CLASS_IN = 0x01
TYPE_CNAME = 0x05
NGINX_CONFIG_DIR = '/etc/nginx/virtualhosts'
CONFIG_PATTERN = '.local.custom.conf'

def publish_cname(cname):
    bus = dbus.SystemBus()
    server = dbus.Interface(bus.get_object(avahi.DBUS_NAME, avahi.DBUS_PATH_SERVER),
            avahi.DBUS_INTERFACE_SERVER)
    group = dbus.Interface(bus.get_object(avahi.DBUS_NAME, server.EntryGroupNew()),
            avahi.DBUS_INTERFACE_ENTRY_GROUP)

    cname = cname + '.local'
    cname = encode_cname(cname)
    rdata = encode_rdata(server.GetHostNameFqdn())
    rdata = avahi.string_to_byte_array(rdata)

    group.AddRecord(avahi.IF_UNSPEC, avahi.PROTO_UNSPEC, dbus.UInt32(0),
        cname, CLASS_IN, TYPE_CNAME, TTL, rdata)
    group.Commit()

def encode_cname(name):
    return '.'.join(ToASCII(p) for p in name.split('.') if p)

def encode_rdata(name):
    def enc(part):
        a = ToASCII(part)
        return chr(len(a)), a
    return ''.join('%s%s' % enc(p) for p in name.split('.') if p) + '\0'

if __name__ == '__main__':
    import time, sys, locale
    # This keeps crashing on startup.  Add a wait (because I'm a lazy dev)
    time.sleep(60)
    # Find the custom dns entries based on the nginx configs
    for filename in os.listdir(NGINX_CONFIG_DIR):
        # Antsle will already be broadcasting antsle10.local through
        # antsle254.local
        # Only load the configs that are marked as custom dns entries
        if (filename.endswith(CONFIG_PATTERN)):
            name = filename[:-len(CONFIG_PATTERN)]
            publish_cname(name)
    try:
        while True: time.sleep(60)
    except KeyboardInterrupt:
        print "Exiting"
        sys.exit(0)