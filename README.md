# m-captive
Micro captive portal for home networks

This little captive portal enables parents to control the Internet usage of their childreen in a home network. It consists of three components:

1. a DHCP/DNS server (dnsmasq)
1. a set of iptables rules
1. a little Django application which implements a captive portal

The setup is intended to run on a Raspberry Pi with Raspbian, but any other Linux based computer can do the job on the home network.

The overall solution is depicted here:

![Solution overview](http://bit.ly/2YWeapN)

1. DHCP is turned off on the home router
1. DHCP on Pi configures alternate default gateway for kids terminals (_the Pi iteself_)
1. kids access is controlled by a firewall (iptables rules) on teh Pi
1. firewall rules are managed by m-captive (Django webapp behing NGINX on the Pi)

This enables:
- time based access
- whitelisting, blacklisting

# TODO

A lot:
- [ ] Ansible deployment playbook
- [ ] separate Django
- [ ] wsgi in NGINX instead of a reverse proxy
- [ ] detailed user guide (how to manage timers) 
