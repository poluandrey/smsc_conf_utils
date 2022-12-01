import argparse


def argument_parser():
    parser = argparse.ArgumentParser(
        description='cli for checking and loading smpp_rules.conf and sccp_gt_list.dat',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparser = parser.add_subparsers(help='list of commands')
    check_config_parser = subparser.add_parser(
        'check',
        help='check provided config. Return duplicated gt or sme id if them exists',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    check_config_parser.add_argument(
        '--config',
        choices=('smpp', 'sccp_gt'),
        required=True,
    )

    subparser.add_parser(
        'load',
        help='load provided config into DB',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '--file', '-f',
        help='path to file',
        required=True
    )
    return parser.parse_args()


def smpp_conf_parser(conf_path):
    pass


def sccp_gt_parser(conf_path):
    pass


def db_loader(smpp_rules, gt_lis):
    pass


def check_conf_correct(conf_path):
    pass


def main():
    cli = argument_parser()


if __name__ == '__main__':
    print('start')
    main()
