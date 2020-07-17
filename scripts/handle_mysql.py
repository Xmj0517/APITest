import pymysql
import random
from scripts.handle_yaml import do_yaml

class HandleMysql:
    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect(host=do_yaml.read_yaml('mysql', 'host'),  # mysql服务器ip或者域名
                                    user=do_yaml.read_yaml('mysql', 'user'),  # 用户名
                                    password=do_yaml.read_yaml('mysql', 'password'),  # 密码
                                    db=do_yaml.read_yaml('mysql', 'db'),  # 要连接的数据库名
                                    port=do_yaml.read_yaml('mysql', 'port'),  # 数据库端口号，默认为3306
                                    charset='utf8',  # 数据库编码为utf8，不能写成utf-8
                                    cursorclass=pymysql.cursors.DictCursor  # 游标类型设置,使返回数据为字典
                                    )
        # 创建游标对象
        self.cursor = self.conn.cursor()

    def run(self, sql, args=None, is_more=False):
        self.cursor.execute(sql, args)
        self.conn.commit()
        if is_more:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.conn.close()

    @staticmethod
    def create_mobile():
        '''随机生成手机号'''
        return '188' + ''.join(random.sample('0123456789', 8))

    def is_existed_mobile(self, mobile):
        '''
        判断生成的手机号是否已经存在
        :param mobile: mobile是待查询的手机号
        :return: 手机号能查到存在返回True，不存在返回Fales
        '''
        sql = do_yaml.read_yaml('mysql', 'select_user_sql')
        if self.run(sql, args=[mobile]):
            return True
        else:
            return False

    def create_not_existed_mobile(self):
        '''
        随机生成一个数据库中不存在的手机号
        :return:
        '''
        while True:
            one_mobile = self.create_mobile()
            if not self.is_existed_mobile(one_mobile):
                break
        return one_mobile


if __name__ == "__main__":
    # 封装好后自测一下
    sql_1 = "SELECT * FROM futureloan.member WHERE mobile_phone = '13888888888';"
    sql_3 = "SELECT * FROM member LIMIT 0, 10;"

    do_mysql = HandleMysql()
    # print(do_mysql.run(sql_3))
    # print(do_mysql.is_existed_mobile('13888888836'))

    print(do_mysql.create_not_existed_mobile())
    do_mysql.close()
