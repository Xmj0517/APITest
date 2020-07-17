import re

import scripts.handle_excel
# 正则表达式相当于一个模子，可以从文本中找出符合要求的内容
from scripts.handle_mysql import HandleMysql


# 创建替换的字符串
# 定义生成有效字符串的类
class HandleRe(object):
    def __init__(self, one_str):
        '''
        初始化参数
        :param one_str: 由excel传入的一条data数据
        '''
        self.one_str = one_str

    # 处理data，加入有效的手机号
    def replace_phone(self):
        # 创建正则表达式，一定要加r，有特殊字符需要在字符串前方加\
        # match方法，传入正则表达式，待查询字符串
        # match只能从头开始匹配，匹配不到返回None
        # 匹配上后会返回match对象，用group获取结果
        try:
            # 替换生成的手机号
            do_mysql = HandleMysql()
            real_existed_phone = do_mysql.create_not_existed_mobile()
            data_str = re.sub(r"{not_existed_phone}", real_existed_phone, self.one_str)
            do_mysql.close()
            return data_str
        except AttributeError as e:
            data_str = self.one_str
            return data_str


if __name__ == "__main__":
    one_str = '{"mobile_phone": "{not_existed_phone}", "pwd": "12345678", "type": 1, "reg_name": "Xmj"}'
    test_str = HandleRe(one_str)
    res = test_str.replace_phone()
    print(res)


