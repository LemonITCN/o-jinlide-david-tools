import json
import sys

import exit_module
import global_data_module

CONFIG_DATA_KEY = 'config'


def read_config_file():
    print('尝试读取配置文件内容...')
    file_path = parse_config_file_path()
    try:
        file = open(file_path, 'r+')
        config_dic = json.loads(file.read())
        file.close()
        return config_dic
    except FileNotFoundError:
        print('指定的配置文件并不存在: ', file_path)
        exit_module.tip_and_wait_then_exit('读取配置文件失败，无法继续执行采集任务，请按回车键退出程序...')


def parse_config_file_path():
    if len(sys.argv) == 1:
        print('当前未指定配置文件路径，尝试寻找当前目录下的config.json文件')
        return './config.json'
    else:
        print('用户指定配置文件: ', sys.argv[1])
        return sys.argv[1]


def get_config_obj():
    if not global_data_module.contain_key(CONFIG_DATA_KEY):
        global_data_module.set_value(CONFIG_DATA_KEY, read_config_file())
    return global_data_module.get_value(CONFIG_DATA_KEY)
