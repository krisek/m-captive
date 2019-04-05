This document describes the installation of the Pi-captive captive portal on Raspbian.

# static ip configuration for the Pi

        allow-hotplug eth0
        iface eth0 inet static
            address 192.168.188.2
            netmask 255.255.255.0
            gateway 192.168.188.1

Adopt the address/netmask/gateway values as per your home network. Address is referred as $own_ip in this guide.

TODO: turn everything from here to an Ansible playbook

# Software installation

## Packages
        apt install dnsmasq python-virtualenv dnsutils nginx net-tools fish git conntrack

## Pi-captive
        git clone https://github.com/kris/m-captive

# Captive portal customization

        cd m-captive

Files to customize/edit/cp:

1. iptables.save: update $own_ip
1. env/bin/redo.fish: update destination folder if not installed under ~pi/hotspot
1. create new Django superuser (to be able to manage clients)
   
        . env/bin/activate
        cd captive/
        python manage.py createsuperuser 
        ...
        cd ..

4. customize DHCP/DNS configuration: 

        sudo cp etc/dnsmasq.d/captive /etc/dnsmasq.d/captive

update $own_ip & fine tune (add known mac addresses accordingly)

update the captive.portal address and uplink DNS

        address=/captive.portal/$own_ip
        server=8.8.8.8 #optional

5. customize NGINX configuration

        sudo cp etc/nginx/sites-available/default  /etc/nginx/sites-available/default

update hotspot users as per DHCP configuration    
    
6. update captive/welcome/views.py with know devices
7. captive/captive/settings.py: remove * from ALLOWED_HOSTS if everything works fine

# Application startup

1. Enable and start dnsmasq: `sudo systemctl enable dnsmasq; sudo systemctl start dnsmasq`
1. Enable and start NGINX: `sudo systemctl enable nginx; sudo systemctl start nginx`
1. Initialise the firewall: `sudo ./ip_init`
1. Start the captive portal application: `cd captive; nohup bash ./startup.sh`

