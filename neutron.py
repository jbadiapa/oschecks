import argparse
import sys
import os

parser = argparse.ArgumentParser(description='Check the  neutron service')

parser.add_argument('--os-api-version', metavar='api_version', type=str,
                        default="2.0",
                        help='Version of the api'
                        + '2.0 by default it can also be set to 2')

parser.add_argument('--os-auth-url', metavar='URL', type=str,
                        default=os.getenv('OS_AUTH_URL'),
                        help='Keystone URL')

parser.add_argument('--os-username', metavar='username', type=str,
                        default=os.getenv('OS_USERNAME'),
                        help='username to use for authentication')

parser.add_argument('--os-password', metavar='password', type=str,
                        default=os.getenv('OS_PASSWORD'),
                        help='password to use for authentication')

parser.add_argument('--os-tenant', metavar='tenant', type=str,
                        default=os.getenv('OS_TENANT_NAME'),
                        help='tenant name to use for authentication')

parser.add_argument('--os-endpoint-url', metavar='endpoint_url', type=str,
                        help='Override the catalog endpoint.')

parser.add_argument('--timeout', metavar='timeout', type=int,
                        default=120,
                        help='Max number of second to create/delete a '
                        + 'floating ip (120 by default).')

parser.add_argument('--verbose', action='count',
                       help='Print requests on stderr.')

args = parser.parse_args()

from neutronclient.neutron import client as neutron
from neutronclient.common.exceptions import ConnectionFailed


try:
    neutron_client = neutron.Client(args.os_api_version,username=args.os_username,tenant_name=args.os_tenant,
                                    auth_url=args.os_auth_url,password=args.os_password,endpoint_url=args.os_endpoint_url)
    neutron_client.list_networks()
except ConnectionFailed as e:
    splits = str(e).split(':')
    error={}
    if len(splits)>2:
        error['msg']= splits[0]
        error['cause']=splits[1]
        print error['msg'],error['cause']
        sys.exit(2)
print "OK"
sys.exit(0)

