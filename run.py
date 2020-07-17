import unittest
from datetime import datetime
import os

from libs.HTMLTestRunnerNew import HTMLTestRunner
from scripts.handle_yaml import do_yaml
# 导入存放报告的路径
from scripts.handle_path import REPORTS_DIR, USER_ACCOUNTS_FILE_DIR, CASES_DIR
# 导入初始化三个用户的模块
from scripts.handle_user import UserInit

# 运行测试前先判断用户是否已经有初始化，存在目录则不需要执行初始化
if not os.path.exists(USER_ACCOUNTS_FILE_DIR):
    UserInit.user_init()

# 创建测试套件
# suite = unittest.TestSuite()
#
# # 加载用例到测试套件
# loader = unittest.TestLoader()
# suite.addTest(loader.loadTestsFromModule(test_register_case))
# suite.addTest(loader.loadTestsFromModule(test_login_case))

suite = unittest.defaultTestLoader.discover(CASES_DIR)


# 添加报告路径
result_full_path = do_yaml.read_yaml('report', 'report_name') + '_' + \
                   datetime.strftime(datetime.now(), '%Y%m%d%H%M%S') + '.html'
result_full_path = os.path.join(REPORTS_DIR, result_full_path)

with open(result_full_path, 'wb') as f:
    runner = HTMLTestRunner(stream=f,
                            title=do_yaml.read_yaml('report', 'title'),
                            description=do_yaml.read_yaml('report', 'description'),
                            tester=do_yaml.read_yaml('report', 'tester'))
    runner.run(suite)
