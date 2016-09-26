#!/usr/bin/env python
#
# Dynamic dns tool
# usage: dyn_dns $HOSTED_ZONE_ID $DNS_NAME
# example: dyn_dns 3213124 www.mysite.com
#
# to schedule see https://www.raspberrypi.org/documentation/linux/usage/cron.md
#
import botocore.session
import json
import sys

import requests

session = botocore.session.get_session()
client = session.create_client('route53')


def get_my_ip():
    return json.loads(requests.get("http://api.ipify.org?format=json").content)['ip']

response = client.change_resource_record_sets(
    HostedZoneId=sys.argv[1],
    ChangeBatch={
        'Comment': 'string',
        'Changes': [
            {
                'Action': 'UPSERT',
                'ResourceRecordSet': {
                    'Name': sys.argv[2],
                    'Type': 'A',
                    'TTL': 300,
                    'ResourceRecords': [
                        {
                            'Value': get_my_ip()
                        },
                    ],
                }
            },
        ]
    })
