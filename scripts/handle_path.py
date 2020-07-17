import os

# # 获取当前文件的绝对路径
# one_path = os.path.abspath(__file__)
# # 获取当前文件的上一级目录
# two_path = os.path.dirname(one_path)
# # 获取项目根路径
# three_path = os.path.dirname(two_path)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 获取配置文件夹所在的路径
CONFIGS_DIR = os.path.join(BASE_DIR, 'configs')

# 获取配置文件所在的路径
CONFIG_FILE_DIR = os.path.join(CONFIGS_DIR, 'testcase.yaml')

# 获取日志文件所在的目录路径
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# 获取报告文件所在的目录路径
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

# 获取excel文件所在的目录路径
DATAS_DIR = os.path.join(BASE_DIR, 'datas')

# 获取用户账号所在配置文件的路径
USER_ACCOUNTS_FILE_DIR = os.path.join(CONFIGS_DIR, 'user_info.yaml')

# 用例所在目录
CASES_DIR = os.path.join(BASE_DIR, 'cases')

# pass
# print(one_path)
