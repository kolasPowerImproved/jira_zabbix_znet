import re
from pprint import pprint

from pyzabbix import ZabbixAPI, ZabbixAPIException
from jira.client import JIRA
from consts import SERVER_ZABBIX, LOGIN_ZABBIX, PASSWORD_ZABBIX, SERVER_JIRA, LOGIN_JIRA, PASSWORD_JIRA

# connect to the zabbix
z = ZabbixAPI(SERVER_ZABBIX)
z.login(user=LOGIN_ZABBIX, password=PASSWORD_ZABBIX)

# connect to the jira
jira_options = {'server': SERVER_JIRA}
jira = JIRA(options=jira_options, basic_auth=(LOGIN_JIRA, PASSWORD_JIRA))

issues = jira.search_issues('project = ZNET AND NOT status = Canceled AND NOT status = Closed', maxResults=100)
list_issue = []  # empty list for znet numbers
for issue in issues:
    list_issue.append(issue.key)  # add znet issue

# pprint(list_issue)

# find host in group ZNET (id=37)
hosts = z.host.get(groupids=[37])

list_host_names = []  # empty list with hosts names
for host in hosts:
    list_host_names.append(host['name'])

hosts_for_not_delete = []
hosts_for_delete = []
for host in list_host_names:
    for issue in list_issue:
        if re.search(issue, host) is not None:
            hosts_for_not_delete.append(host)

for host in list_host_names:
    if host not in hosts_for_not_delete:
        hosts_for_delete.append(host)

ids_for_delete = []
for host in hosts_for_delete:
    host = z.do_request(method='host.get', params={"filter": {"host": host}, "output": ["hostid"]})
    ids_for_delete.append(host["result"])
# pprint(ids_for_delete)

for id in ids_for_delete:
    if id:
        pprint(id[0]["hostid"])
        # z.host.delete(id[0]["hostid"])                # uncomment for deleting hosts
        pprint("zbs")
