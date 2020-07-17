import re
import os

from scripts.handle_mysql import HandleMysql
from scripts.handle_yaml import HandleYaml
from scripts.handle_path import USER_ACCOUNTS_FILE_DIR, CONFIG_FILE_DIR


class HandleParam:
    '''
    参数化类
    '''
    # 不存在的参数
    not_existed_phone_pattern = r"{not_existed_phone}"  # 不存在的手机号
    not_existed_id = r"{not_existed_user_id}"  # 不存在的用户id
    not_existed_loan_id_pattern = r'{not_existed_loan_id}'  # 不存在的loan id

    # 投资人参数
    invest_existed_phone_pattern = r"{invest_existed_phone}"  # 投资人手机号
    invest_user_pwd_pattern = r"{invest_user_pwd}"  # 投资人密码
    invest_user_id_pattern = r"{invest_user_id}"  # 投资人id

    # 借款人参数
    borrow_existed_phone_pattern = r"{borrow_existed_phone}"  # 借款人手机号
    borrow_user_pwd_pattern = r"{borrow_user_pwd}"  # 借款人密码
    borrow_user_id_pattern = r"{borrow_user_id}"  # 借款人id

    # 管理员参数
    admin_existed_phone_pattern = r"{admin_existed_phone}"  # 管理员手机号
    admin_user_pwd_pattern = r"{admin_user_pwd}"  # 管理员密码

    # 其他参数
    loan_id_pattern = r"{loan_id}"  # 标id

    do_yaml = HandleYaml(CONFIG_FILE_DIR)
    do_user_account = HandleYaml(USER_ACCOUNTS_FILE_DIR)

    # 不存在的参数替换
    @classmethod
    def not_existed_replace(cls, data):
        cls.do_mysql = HandleMysql()
        # 不存在的手机号替换
        if cls.not_existed_phone_pattern in data:  # 这里成员运算效率较高
            data = re.sub(cls.not_existed_phone_pattern, \
                          cls.do_mysql.create_not_existed_mobile(), data)

        # 替换不存在的用户id
        if re.search(cls.not_existed_id, data):
            # 从数据库中取出最大id，然后加1即为不存在的id
            sql = "SELECT id FROM member ORDER BY id DESC LIMIT 0,1;"
            max_id = cls.do_mysql.run(sql)
            data = re.sub(cls.not_existed_id, str(max_id['id'] + 1), data)

        # 不存在的load_id替换
        if cls.not_existed_loan_id_pattern in data:
            sql = "SELECT id FROM loan ORDER BY id DESC LIMIT 0, 1;"
            not_existed_load_id = cls.do_mysql.run(sql).get('id') + 1  # 获取最大的用户id + 1
            data = re.sub(cls.not_existed_loan_id_pattern, str(not_existed_load_id), data)

        cls.do_mysql.close()
        return data

    # 投资人参数替换
    @classmethod
    def invest_replace(cls, data):
        # 投资人手机号参数化替换
        if re.search(cls.invest_existed_phone_pattern, data):
            data = re.sub(cls.invest_existed_phone_pattern, \
                          cls.do_user_account.read_yaml('投资人', 'mobile_phone'), data)

        # 投资人密码参数化替换
        if re.search(cls.invest_user_pwd_pattern, data):
            data = re.sub(cls.invest_user_pwd_pattern, \
                          cls.do_user_account.read_yaml('投资人', 'pwd'), data)

        # 投资人id替换
        if re.search(cls.invest_user_id_pattern, data):
            data = re.sub(cls.invest_user_id_pattern, \
                          str(cls.do_user_account.read_yaml('投资人', 'id')), data)

        return data

    # 借款人参数替换
    @classmethod
    def borrow_replace(cls, data):
        # 借款人手机号参数化替换
        if re.search(cls.borrow_existed_phone_pattern, data):
            data = re.sub(cls.borrow_existed_phone_pattern, \
                          cls.do_user_account.read_yaml('借款人', 'mobile_phone'), data)

        # 借款人密码参数化替换
        if re.search(cls.borrow_user_pwd_pattern, data):
            data = re.sub(cls.borrow_user_pwd_pattern, \
                          cls.do_user_account.read_yaml('借款人', 'pwd'), data)

        # 借款人id替换
        if re.search(cls.borrow_user_id_pattern, data):
            data = re.sub(cls.borrow_user_id_pattern, \
                          str(cls.do_user_account.read_yaml('借款人', 'id')), data)

        return data

        #

    # 管理员参数替换
    @classmethod
    def admin_replace(cls, data):
        # 管理员手机号参数化替换
        if re.search(cls.admin_existed_phone_pattern, data):
            data = re.sub(cls.admin_existed_phone_pattern, \
                          cls.do_user_account.read_yaml('管理员', 'mobile_phone'), data)

        # 借款人id替换
        if re.search(cls.admin_user_pwd_pattern, data):
            data = re.sub(cls.admin_user_pwd_pattern, \
                          str(cls.do_user_account.read_yaml('管理员', 'pwd')), data)

        return data

    # 其他参数替换
    @classmethod
    def other_replace(cls, data):
        # load_id替换
        if re.search(cls.loan_id_pattern, data):
            loan_id = getattr(cls, 'loan_id')
            data = re.sub(cls.loan_id_pattern, str(loan_id), data)
        return data


    @classmethod
    def to_param(cls, data):
        data = cls.not_existed_replace(data)
        data = cls.invest_replace(data)
        data = cls.borrow_replace(data)
        data = cls.admin_replace(data)
        data = cls.other_replace(data)

        return data


if __name__ == "__main__":
    one_str = '{"mobile_phone": "{invest_user_id}", "pwd": "12345678", "type": 1, "reg_name": "Xmj"}'
    two_str = '{"member_id": {not_existed_user_id}, "amount": 6300}'
    print(HandleParam.to_param(two_str))
