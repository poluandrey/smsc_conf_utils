import os
from pathlib import Path
from main import gt_conf_parser, check_gt_conf, check_smpp_conf, smpp_conf_parser

import pytest


@pytest.fixture
def gt_conf_file(request):
    conf_type = request.param
    if 'bad_gt' == conf_type or 'relative_path' == conf_type:
        file = Path('test_conf/bad_sccp_gt_list.dat')
    elif 'good_gt' == conf_type:
        file = Path('test_conf/good_sccp_gt_list.dat')
    elif 'good_smpp' == conf_type:
        file = Path('test_conf/good_smpp_rules.ini')
    elif 'bad_smpp' == conf_type:
        file = Path('test_conf/bad_smpp_rules.ini')
    elif 'absolute_path' == conf_type:
        file = os.path.abspath(Path('test_conf/bad_sccp_gt_list.dat'))
    return file


@pytest.mark.parametrize('gt_conf_file, result',
                         [
                             ('bad_gt', 6),
                             ('good_gt', 3),
                             ('absolute_path', 6),
                             ('relative_path', 6),
                         ],
                         indirect=['gt_conf_file']
                         )
def test_gt_conf_parser(gt_conf_file, result):
    parsed_conf = gt_conf_parser(gt_conf_file)
    assert len(parsed_conf) == result, f'Wrong count of line in parsed conf. Expected 6 got {len(parsed_conf)}'

@pytest.mark.parametrize('gt_conf_file, result',
                         [
                             ('bad_smpp', 'WARNING'),
                             ('good_smpp', 'All looks good'),
                         ],
                         indirect=['gt_conf_file']
                         )
def test_check_smpp_conf(gt_conf_file, result):
    parsed_conf = smpp_conf_parser(gt_conf_file)
    check_result = check_smpp_conf(parsed_conf)
    assert check_result.startswith(result), f'Bad config file checking. Answer did not contain {result}'

@pytest.mark.parametrize('gt_conf_file, result',
                         [
                             ('bad_gt', 'WARNING'),
                             ('good_gt', 'All looks good'),
                         ],
                         indirect=['gt_conf_file']
                         )
def test_check_gt_conf(gt_conf_file, result):
    parsed_conf = gt_conf_parser(gt_conf_file)
    check_result = check_gt_conf(parsed_conf)
    assert check_result.startswith(result), f'Bad config file checking. Answer did not contain {result}'
