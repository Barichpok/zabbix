#!/usr/bin/env python

import subprocess
import sys
import logging
import random
import string

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('/var/log/zabbix/soapui.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def session_id_generator(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def main():
    xml_file = "/usr/lib/zabbix/externalscripts/test.xml"
    report_dir = "/usr/lib/zabbix/externalscripts/reports"
    test_case = sys.argv[1]
    command_opts = "-c " + "\"" + test_case + "\" -r " + xml_file + " -f " + report_dir

    command = subprocess.Popen(['/opt/app/soapui/SoapUI-5.3.0/bin/testrunner.sh %s' % command_opts],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=True)

    key = None

    rnd = session_id_generator()

    for line in command.stdout:
        line = str(line.strip())
        logger.info('SessionID (%s) = %s', rnd, line)
        if line.__contains__("finished with status [FINISHED]"):
            key = 0

    if key == 0:
        return 0
    else:
        return 1

if __name__ == "__main__":
    main()

# /usr/lib/zabbix/externalscripts
# sudo -u zabbix python soapui.py 'TestCase 1'
