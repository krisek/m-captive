# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
import re
import logging
from wifi_user import wifi_user
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
import subprocess
import sys
import collections
from background_task import background
from datetime import timedelta
import time

# Create your views here.

logger = logging.getLogger(__name__)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

users = {
    '4c:49:e3:b6:ef:a7': 'Adel',
    '64:cc:2e:6e:ee:89': 'Lori',
    'b4:9d:0b:6d:59:b8': 'Kris',
    '5c:51:88:3a:af:9c': 'Vera',
    '9c:b6:d0:e2:09:d1': 'xps13',
    '18:3d:a2:08:4f:98': 'x201',
    '10:6b:1c:10:18:0c': 'Irulu',
    '04:b1:67:6e:99:ae': 'Adam',
    '60:67:20:ed:42:8c': 't430s',
    '10:0b:a9:62:06:60': 'e4310',
    '74:c2:46:be:99:51': 'FireTV',
    '74:04:2b:e8:ee:d5': 'Lenovo A10',
    '20:54:76:5d:bb:c4': 'st27i',
    'c8:d3:ff:56:7e:7e': 'hp-deskjet-3700',
    'd8:50:e6:2d:d1:55': 'nexus7',
    '00:e0:4c:a0:10:12': 'scanpi'
    }

timed_users = {
    'Adel': True,
    'Lori': True,
    'Adam': True,
    't430s': True,
    'e4310': True,
    'Guest': True,
    'Lenovo A10': True,
}

emergency_users = {
}

emergency_access = {}

from django.http import JsonResponse

def ajax(request):
    data = {}
    data['something'] = 'useful'
    return JsonResponse(data)

class AdminView(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        #list users
        users_wifi = collections.OrderedDict()
        f = open("/var/lib/misc/dnsmasq.leases", "r")

        for line in f:
            info_elems = line.split(r' ')
            user = {'mac': info_elems[1],
                    'ip': info_elems[2],
                    'hostname': info_elems[3],
                    'timestamp': info_elems[0],
                    'chains': {}}
            if(user['mac'] in users):
                user['name'] = users[user['mac']]
            else:
                user['name'] = 'Guest'
            users_wifi[user['mac']] = user;
        f.close()

        for mac in users:
            if(mac not in users_wifi):
                user = {
                    'mac': mac,
                    'ip': 'inactive',
                    'hostname': 'unknown',
                    'name': users[mac],
                    'timestamp': None,
                    'chains': {}
                    }
                users_wifi[user['mac']] = user;

        for chain in ['internet', 'web']:
            chain_str = subprocess.check_output(["sudo","iptables","-L",chain,"-t","mangle"],universal_newlines=True)
            chain_data=chain_str.split('\n')
            for line in chain_data:
                matchObj = re.search(r'MAC ([^\s]+)', line)
                if(matchObj and matchObj.group(1).lower() in users_wifi):
                    users_wifi[matchObj.group(1) .lower()]['chains'][chain] = True

        d = {"wiusers": users_wifi}
        return render(request, 'admin.html', context=d)

class AdminManageView(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        selector = request.GET['selector']
        wiuser = wifi_user(users, selector)
        if(re.search(r'enable$', request.META['PATH_INFO'])):
            wiuser.traffic_enable()
            #echo "python3 /home/kris/projects/hotspot/userinet.py -u wiuser.mac -a enable" | at 'now + 1 minutes'
            #invalidate emergency access control
            if(wiuser.name in timed_users):
                try:
                    timeout = int(request.GET['timeout'])
                except:
                    timeout = 30

                disable_user(selector, schedule=timedelta(minutes=timeout))
        else:
            wiuser.traffic_disable()
        return redirect('/welcome/wifiadmin/')

class EmergencyAccessView(TemplateView):
    def get(self, request, **kwargs):
        selector = request.GET['selector']
        wiuser = wifi_user(users, selector)
        if(wiuser.mac not in emergency_access or int(time.time())-emergency_access[wiuser.mac] > 3420):
            wiuser.traffic_enable()
            disable_user(selector, schedule=timedelta(minutes=1))
            emergency_access[wiuser.mac] = int(time.time())
        return redirect(request.GET['url'])

@background(schedule=timedelta(minutes=30))
def disable_user(selector):
    wiuser = wifi_user(users, selector)
    wiuser.traffic_disable()

class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        ip = get_client_ip(request)
        wiuser = wifi_user(users, ip)
        d = {"wiuser": wiuser}
        if 'url' in request.GET:
            d['url'] = request.GET['url']
        if(wiuser.mac not in emergency_access or int(time.time())-emergency_access[wiuser.mac] > 3420):
             d['emergency_enabled'] = True
        return render(request, 'index.html', context=d)

class AboutPageView(TemplateView):
    template_name = "about.html"
