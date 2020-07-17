import os

from scripts.handle_path import USER_ACCOUNTS_FILE_DIR
from scripts.handle_yaml import HandleYaml
from scripts.handle_mysql import HandleMysql
from scripts.handle_request import HandleRequest


class UserInit:
    @classmethod
    def user_init(cls):
        # 获取请求头
        headers = {"X-Lemonban-Media-Type": "lemonban.v2"}
        # 创建请求对象
        do_request = HandleRequest()
        # 添加请求头
        do_request.add_headers(headers)
        # url
        url = 'http://api.lemonban.com/futureloan/member/register'

        # 创建初始三个用户，如果已经创建过则不用再创
        user = [{'mobile_phone': '', 'pwd': '12345678', 'type': 0, 'reg_name': '管理员'},
                {'mobile_phone': '', 'pwd': '12345678', 'type': 1, 'reg_name': '借款人'},
                {'mobile_phone': '', 'pwd': '12345678', 'type': 1, 'reg_name': '投资人'}
                ]

        do_yaml = HandleYaml(USER_ACCOUNTS_FILE_DIR)
        number = HandleMysql()
        new_user = {}
        for i in user:
            i["mobile_phone"] = number.create_not_existed_mobile()
            # 发起请求
            res = do_request.send(url=url, data=i).json()
            # 获取用户id
            new_user['{}'.format(i['reg_name'])] = res['data']
            new_user['{}'.format(i['reg_name'])]['pwd'] = i['pwd']
        # 写入配置文件
        do_yaml.write_yaml(USER_ACCOUNTS_FILE_DIR, new_user)
        # 关闭请求
        do_request.close()
        # 关闭数据库连接
        number.close()


if __name__ == '__main__':
    UserInit.user_init()
    pass
