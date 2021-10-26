import argparse
import sys
from zia_audit_report import get_audit_report


def initialize_parser():
    parser = argparse.ArgumentParser()
    # Global options
    parser = argparse.ArgumentParser()
    parser.add_argument('-24', '--last-24',
                        action='store_true',
                        help='Get audit report for last 24 hours (1440 min) and save result in csv file')
    parser.add_argument('-5', '--last-5',
                        action='store_true',
                        help='Get audit report for last 5 minutes and save result in csv file')
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
    parser.add_argument('-rlog', '--remote_logging',
                        help='Remote syslog server information. Format IP address:protocol:port Example X.X.X.X:TCP:513')

    args = parser.parse_args()
    plugin_selection(args)


def plugin_selection(args):
    """
    Selects the plugin to be used based on the parser
    :param args: parer arguments
    :return:
    """
    if args.last_24:
        if args.remote_logging:
            get_audit_report(args.api_key, args.user, args.password, args.cloud, start_time=1400,
                             rlog=args.remote_logging)
        else:
            get_audit_report(args.api_key, args.user, args.password, args.cloud, start_time=1400)
    elif args.last_5:
        if args.remote_logging:
            get_audit_report(args.api_key, args.user, args.password, args.cloud, start_time=5, rlog=args.remote_logging)
        else:
            get_audit_report(args.api_key, args.user, args.password, args.cloud, start_time=5)


    elif args.version:
        print('zs_audit_report version 1.1')
    else:
        print("invalid command")
        raise ValueError("Invalid command")
