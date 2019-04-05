#!/usr/bin/env bash

cd "$(dirname "$0")"

IPPREV=`cat ip.box`
IP=`dig your_dyndns @8.8.8.8 +short`

echo "deleting old IP $IPPREV from ACL"
iptables -D internet -t mangle  -m iprange --dst-range $IPPREV -j RETURN
iptables -D web -t mangle  -m iprange --dst-range $IPPREV  -j RETURN

echo "adding IP $IP to ACL"
iptables -t mangle -I internet 1 -m iprange --dst-range $IP -j RETURN
iptables -t mangle -I web 1 -m iprange --dst-range $IP -j RETURN

echo $IP > ip.box
