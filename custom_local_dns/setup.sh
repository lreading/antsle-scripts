#!/bin/bash
#
# This file will configure your Antsle to broadcast 
# custom .local DNS entries for your antlets.
# Run this script with -h or --help to learn how to configure them 
#

# TODO: Create a zip or tar.gz archive that has all the setup files
download() {
    echo 'Downloading setup files...'
    echo 'TODO:'
}

extract() {
    echo 'Extracting setup files...'
    echo 'TODO:'
}

restart() {
    echo 'Restarting services...'
    rc-service antlet_local_dns start && service nginx restart
    echo 'Services restarted.  New DNS entries found in '
    echo '/etc/nginx/virtualhosts matching <name>.local.custom.conf'
    echo 'should now be discoverable on your network.'
}

install() {
    echo 'Installing setup files'
    echo 'TODO:'
    
    cp ./antlet_local_dnsd /usr/local/bin/antlet_local_dnsd
    chmod +x /usr/local/bin/antlet_local_dnsd

    cp ./custom_local_dns.py /usr/local/bin/custom_local_dns.py
    chmod +x /usr/local/bin/custom_local_dns.py

    cp ./antlet_local_dns /etc/init.d/antlet_local_dns
    chmod +x /etc/init.d/antlet_local_dns

    # Configure this service to run on boot
    rc-update add /etc/init.d/antlet_local_dns default
    restart()
}

help() {
    echo 'Help: Antlet Custom Local DNS'
    echo ''
    echo 'This script sets up functionality to be able to create'
    echo 'custom .local DNS entries for your antlets'
    echo ''
    echo 'After running this script, you can create an Nginx config'
    echo 'for any antlet by copying the custom.dns.local.template'
    echo 'file to /etc/nginx/virtualhosts/<name>.local.custom.conf'
    echo ''
    echo 'After adding the config, run the following command:'
    echo '      rc-service antlet_local_dns start && service nginx restart'
    echo ''
    echo ''
    echo 'Commands:'
    echo '      -h | --help     Shows the help'
    echo '      -r | --restart  Restarts the service to apply new nginx configs'
    echo '      default         Downloads sources and installs'
}

case "$1" in
    -h | --help)
        help()
        exit 0
        ;;
    -r | --restart)
        restart()
        exit 0
        ;;
    *)
        install()
        exit 0
        ;;
esac
