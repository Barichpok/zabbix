from pyzabbix import ZabbixAPI, ZabbixAPIException
import sys

description = open('C:/Users/Documents/Zabbix/Test_names.txt')
zabbix_server = 'http://zabbix_ip'
zapi = ZabbixAPI(zabbix_server)
zapi.login('login', 'password')
host_name = 'test_name'
hosts = zapi.host.get(filter={"host": host_name}, selectInterfaces=["interfaceid"])


def zabbix_item(method_name):

    if hosts:
        host_id = hosts[0]["hostid"]
        print("Found host id {0}".format(host_id))
        try:
            item = zapi.item.create(
                hostid=host_id,
                name=method_name.strip(),
                key_='soapui.py[' + method_name.strip() + ']',
                type=10,
                value_type=3,
                interfaceid=hosts[0]["interfaces"][0]["interfaceid"],
                delay=3600,
                history=60,
                trends=60
            )
        except ZabbixAPIException as e:
            print(e)
            sys.exit()
        print("Added item with itemid {0} to host: {1}".format(item["itemids"][0], host_name))
    else:
        print("No hosts found")


def zabbix_trigger(method_name):

    if hosts:
        host_id = hosts[0]["hostid"]
        print("Found host id {0}".format(host_id))
        try:
            trigger = zapi.trigger.create(
                description=method_name.strip(),
                expression='{test_name:soapui.py[' + method_name.strip() + '].last()}>0',
                priority=5
            )
        except ZabbixAPIException as e:
            print(e)
            sys.exit()
        print("Added trigger with triggerid {0} to host: {1}".format(trigger["triggerids"][0], host_name))
    else:
        print("No hosts found")


def zabbix_action(parse):

    parameters = {'status': '0',
                  'def_shortdata': 'zabbix',
                  'r_shortdata': 'zabbix',
                  'name': '' + parse['description'] + '',
                  'esc_period': '3600',
                  'def_longdata': 'Trigger: {TRIGGER.NAME}\r\nTrigger status: {TRIGGER.STATUS}',
                  'r_longdata': 'Trigger: {TRIGGER.NAME}\r\nTrigger status: {TRIGGER.STATUS}',
                  'eventsource': '0',
                  'filter': {'evaltype': 0,
                             'conditions': [{'conditiontype': 2,
                                             'value': '' + parse['triggerid'] + ''
                                             }]
                             },
                  'operations': [{'operationtype': 0,
                                  'opmessage_usr': [{'userid': 3},
                                                    {'userid': 4}],
                                  'opmessage': {'default_msg': 1,
                                                'mediatypeid': 0}
                                  }],
                  'recovery_operations': [{'operationtype': 0,
                                           'opmessage_usr': [{'userid': 3},
                                                             {'userid': 4}],
                                           'opmessage': {'default_msg': 1,
                                                         'mediatypeid': 0}
                                           }]
                  }

    if hosts:
        host_id = hosts[0]["hostid"]
        print("Found host id {0}".format(host_id))
        try:
            action = zapi.action.create(parameters)
        except ZabbixAPIException as e:
            print(e)
            sys.exit()
        print("Added action with actionid {0} to host: {1}".format(action["actionids"][0], host_name))
    else:
        print("No hosts found")


if __name__ == "__main__":

    for d in description.readlines():
        zabbix_item(d)
        zabbix_trigger(d)

    description.close()

    for t in zapi.trigger.get(hostids=['10107']):
        zabbix_action(t)
