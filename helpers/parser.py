import argparse
import sys


def initialize_parser():
    parser = argparse.ArgumentParser()
    # Global options
    subparsers = parser.add_subparsers(dest="command")
    # Command: vip-status
    parser_update_device = subparsers.add_parser(
        "vip-status",
        help="Get Virtual Server status and compare pre/post maintenance results",
    )
    parser_update_device.add_argument(
        "-s", "--start-file",
        help="Pre maintenance file with tmsh show ltm virtual recursive /\* | grep -E \'Ltm|Availability|reason\' output",

    )
    parser_update_device.add_argument(
        "-e", "--end-file",
        help="Post maintenance file with tmsh show ltm virtual recursive /\* | grep -E \'Ltm|Availability|reason\' output",

    )
    parser_update_device.add_argument(
        "-pre", "--pre",
        help="Obtain pre maintenance Virtual Server status via iControl REST API",
        action='store_true'
    )
    parser_update_device.add_argument(
        "-post", "--post",
        help="Obtain post maintenance Virtual Server statuses  via iControl REST API and compare with previous results",
        action='store_true'
    )
    # Command: pool-status
    parser_update_device = subparsers.add_parser(
        "pool-status",
        help="Get Pool and Pool member status and compare pre/post maintenance results",
    )
    parser_update_device.add_argument(
        "-s", "--start-file",
        help="Pre maintenance file with tmsh show ltm pool recursive /\* members detail | grep -E \'Ltm|Availability|Pool Member\' output",

    )
    parser_update_device.add_argument(
        "-e", "--end-file",
        help="Post maintenance file with tmsh show ltm pool recursive /\* members detail | grep -E \'Ltm|Availability|Pool Member\' output",

    )
    '''parser_update_device.add_argument(
        "-pre", "--pre",
        help="Obtain pre maintenance Virtual Server status via iControl REST API",
        action='store_true'
    )
    parser_update_device.add_argument(
        "-post", "--post",
        help="Obtain post maintenance Virtual Server statuses  via iControl REST API and compare with previous results",
        action='store_true'
    )'''

    # Command: updates
    parser_updates = subparsers.add_parser(
        "updates",
        help="Customer updates",
    )
    parser_updates.add_argument(
        "-t", "--tap",
        help="TAP updates.",
        action='store_true'
    )
    parser_updates.add_argument('-n', '--name',
                                help='Name',
                                required=True
                                )

    # Command: audit-irules
    parser_audit_irules= subparsers.add_parser(
        "audit-irules",
        help="Audit iRules, events and commands ",
    )

    args = parser.parse_args()
    if not args.command:
        parser.parse_args(["--help"])
        sys.exit(0)
    # Do the stuff here
    print(args)
    plugin_selection(args)

def plugin_selection(args):
    """
    Selects the plugin to be used based on the parser
    :param args: parer arguments
    :return:
    """
    if args.command == 'audit-irules':
        start_process()
    elif args.command == 'updates':
        updates(args)
    elif args.command == 'vip-status':
        maint(args)
    elif args.command == 'pool-status':
        main_pool_status(args)
    else:
        print("invalid command")
        raise ValueError("Invalid command")