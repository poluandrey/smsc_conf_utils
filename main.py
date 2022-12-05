import argparse
import os
import re

from collections import namedtuple

# from typing import List, Tuple


SmppConnections = namedtuple('SmppConnections', 'sme_id, type, system_id, password, system_type')

SmppConfig = namedtuple('SmppConfig', 'connections, rules')


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
    check_config_parser.add_argument(
        '--file', '-f',
        help='path to file',
        required=True
    )
    check_config_parser.set_defaults(callback=check_config_callback)

    subparser.add_parser(
        'load',
        help='load provided config into DB',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    return parser.parse_args()


def gt_conf_parser(in_file):
    parsed_conf = []
    with open(in_file, 'r') as f_in:
        for line in f_in:
            if re.search(r'^\d', line):
                gt_params = re.sub(' +', ' ', line).split(' ')
                gt_id, gt, link = gt_params
                parsed_conf.append(
                    (gt_id.strip(), gt.strip(), link.strip()))
    return parsed_conf


def sme_parser(line):
    params = re.sub(' +', ' ', line).split(' ')
    return SmppConnections(
        params[1],
        params[2].replace('"', ''),
        params[3].replace('"', ''),
        params[4].replace('"', ''),
        params[5].replace('"', '')
    )


def smpp_conf_parser(in_file):
    connections = []
    rules = []
    with open(in_file, 'r') as f_in:
        for line in f_in:
            if re.search('^sme', line):
                connections.append(sme_parser(line.strip()))
            elif re.search('^rule', line):
                pass
    return SmppConfig(connections, rules)


def check_gt_conf(parsed_conf):
    gt_ids = [values[0] for values in parsed_conf]
    unique_ids = list(set(gt_ids))
    for gt_id in unique_ids:
        gt_ids.remove(gt_id)
    if gt_ids:
        return 'WARNING!\n{} ids are duplicated'.format(", ".join(gt_ids))
    return 'All looks good'


def check_smpp_conf(parsed_conf):
    sme_ids = [connection.sme_id for connection in parsed_conf.connections]
    unique_sme_ids = list(set(sme_ids))
    for sme_id in unique_sme_ids:
        sme_ids.remove(sme_id)
    if sme_ids:
        return 'WARNING\n{} sme are duplicated'.format(", ".join(sme_ids))
    return 'All looks good'


def get_file_path(in_file):
    if os.path.isabs(in_file):
        return in_file
    else:
        return os.path.abspath(in_file)


def check_config_callback(arguments):
    file_path = get_file_path(arguments.file)
    if arguments.config == 'smpp':
        parsed_conf = smpp_conf_parser(file_path)
        print(check_smpp_conf(parsed_conf))
    elif arguments.config == 'sccp_gt':
        parsed_conf = gt_conf_parser(file_path)
        print(check_gt_conf(parsed_conf))


def db_loader(smpp_rules, gt_lis):
    pass


def main():
    args = argument_parser()
    args.callback(args)


if __name__ == '__main__':
    main()
