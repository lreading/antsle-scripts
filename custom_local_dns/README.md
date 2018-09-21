# Custom Local DNS Entries
These scripts are a jumping-off point for creating your own custom .local DNS entries for your antlets.
Following the steps described here will allow you to assign a .local address to an antlet while maintaining the antletxx.local entry.

# Setup
1 SSH into your Antsle
2 Copy antlet_local_dnsd to /usr/local/bin/antlet_local_dnsd and grant execute permissions (chmod +x /usr/local/bin/antlet_local_dnsd.py)
3 Copy custom_local_dns.py to /usr/local/bin/custom_local_dns.py and grant execute permissions (chmod +x /usr/local/bin/custom_local_dns.py)
4 Copy antlet_local_dns to /etc/init.d/antlet_local_dns and grant execute permissions (chmod +x /etc/init.d/antlet_local_dns)
5 Run the following to have the service start on boot: `rc-update add /etc/init.d/antlet_local_dns default`
6 Reboot the system OR start the service `rc-service antlet_local_dns start`
7 Make a new Nginx config for your .local domain and put it in `/etc/nginx/virtualhosts`.  BE SURE TO UPDATE THE PROPERTIES AND NAME IT WITH THE FOLLOWING CONVENTION: `<name>.local.custom.conf`
8 Restart the antlet_local_dns service and the nginx service `rc-service antlet_local_dns restart && service nginx restart`