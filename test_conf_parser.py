from pathlib import Path
from main import gt_conf_parser, check_gt_conf

import pytest


@pytest.fixture
def gt_conf_file(request):
    conf_type = request.param
    if 'bad' == conf_type or 'relative_path' == conf_type:
        file = Path('conf/bad_sccp_gt_list.dat')
    elif 'good' == conf_type:
        file = Path('conf/good_sccp_gt_list.dat')
    elif 'absolute_path' == conf_type:
        file = Path('/Users/andrey/Documents/work/smsc_conf_parser/conf/bad_sccp_gt_list.dat')
    return file


@pytest.mark.parametrize('gt_conf_file, result',
                         [
                             ('bad', 6),
                             ('good', 3),
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
                             ('bad', 'WARNING'),
                             ('good', 'All looks good'),
                         ],
                         indirect=['gt_conf_file']
                         )
def test_check_gt_conf(gt_conf_file, result):
    parsed_conf = gt_conf_parser(gt_conf_file)
    check_result = check_gt_conf(parsed_conf)
    assert check_result.startswith(result), f'Bad config file checking. Answer did not contain {result}'
