import argparse
import sys
from zia_audit_report import get_audit_report


def initialize_parser():
    parser = argparse.ArgumentParser()
    # Global options
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--default',
                        action='store_true',
                        help='get audit report for last 24 hours and save result in CSV file')
    parser.add_argument('-a', '--api_key',
                        help='ZIA API key',
                        required=True)
    parser.add_argument('-u', '--user',
                        help='ZIA username (emailaddress)',
                        required=True)
    parser.add_argument('-p', '--password',
                        help='ZIA password',
                        required=True)
    parser.add_argument('-c', '--cloud',
                        help='ZIA cloud',
                        required=True)
    parser.add_argument('-v', '--version',
                        action='store_true',
                        help='show the version information and exit')

    args = parser.parse_args()
    plugin_selection(args)


def plugin_selection(args):
    """
    Selects the plugin to be used based on the parser
    :param args: parer arguments
    :return:
    """
    if args.default:
        get_audit_report(args.api_key, args.user, args.password, args.cloud)
    elif args.version:
        print('zs_audit_report version 1.1')
    else:
        print("invalid command")
        raise ValueError("Invalid command")
