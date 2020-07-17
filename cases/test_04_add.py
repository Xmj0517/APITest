import unittest
import os
import json
# import time

# from scripts.handle_re import HandleRe
from libs.ddt import ddt, data
from scripts.handle_parameterize import HandleParam
from scripts.handle_excel import HandleExcel
from scripts.handle_log import do_log
from scripts.handle_yaml import do_yaml
# from scripts.handle_path import DATAS_DIR
from scripts.handle_request import HandleRequest
from scripts.handle_mysql import HandleMysql


@ddt
class TestAdd(unittest.TestCase):
    '''
    测试加标功能
    '''
    excel = HandleExcel('add')
    cases = excel.read_data_obj()

    @classmethod
    def setUpClass(cls):
        cls.do_request = HandleRequest()
        # 添加请求头
        cls.do_request.add_headers(do_yaml.read_yaml('api', 'version'))

    @classmethod
    def tearDownClass(cls):
        cls.do_request.close()

    @data(*cases)
    def test_add(self, case):
        # 将期望结果取出
        expected = case.expected
        # 参数化，将取出来的字符串进行参数替换（如果需要的话）
        data_str = HandleParam.to_param(case.data)

        # 拼接url
        url = do_yaml.read_yaml('api', 'url') + case.url

        # 向接口发起请求
        res = self.do_request.send(url=url,
                                   method=case.request_method,
                                   data=data_str
                                   )
        # 获取的报文转换为字典
        result = res.json()
        msg = case.title  # 获取用例标题
        success_msg = do_yaml.read_yaml('msg', 'success_result')
        fail_msg = do_yaml.read_yaml('msg', 'fail_result')
        row = case.case_id + 1

        # assertEqual第三个参数为用例执行失败之后的提示信息
        try:
            self.assertEqual(expected, result['code'], msg=msg)
        except AssertionError as e:
            # 将用例执行结果写入到result_col列
            do_log.info('{}用例执行有误'.format(case.title))
            self.excel.write_data(row=row,
                                  column=do_yaml.read_yaml('excel', 'result_col'),
                                  value=fail_msg)
            do_log.error('具体异常为{}'.format(e))
            raise e
        else:
            do_log.info('{}用例执行通过'.format(case.title))
            self.excel.write_data(row=row,
                                  column=do_yaml.read_yaml('excel', 'result_col'),
                                  value=success_msg)
            # 判断返回报文中是否有token，如果有则将token取出加入到请求头中
            if 'token_info' in res.text:
                self.do_request.add_headers({"Authorization": \
                                            "Bearer " + result['data']['token_info']['token']})
        finally:
            # 将响应实际结果写入到actual_col列
            self.excel.write_data(row=row,
                                  column=do_yaml.read_yaml('excel', 'actual_col'),
                                  value=res.text
                                  )


if __name__ == "__main__":
    red = TestAdd()
