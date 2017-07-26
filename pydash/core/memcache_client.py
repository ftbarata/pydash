import pylibmc
import simplejson as json
from django.conf import settings


def GetIssues():

    mc = pylibmc.Client([settings.MEMCACHE_SERVER], binary=True, behaviors={"tcp_nodelay": True, "ketama": True})
    str_issues = (mc.get('data:zabbix.issues').decode('utf-8'))

    json_issues = json.loads(str_issues)
    return json_issues

