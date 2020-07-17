import yaml
# 直接导入配置文件路径使用
from scripts.handle_path import CONFIG_FILE_DIR


class HandleYaml(object):
    def __init__(self, filename):
        self.filename = filename

    # 读取数据
    def read_yaml(self, area, option):
        with open(self.filename, encoding='utf8') as file_1:
            data = yaml.full_load(file_1)
            return data[area][option]

    # 写入数据
    @staticmethod
    def write_yaml(filename, datas):
        with open(filename, 'w', encoding='utf8') as file_2:
            yaml.dump(datas, file_2, allow_unicode=True)


# do_yaml = HandleYaml(r'E:\pythonlearning\APITest\configs\testcase.yaml')
do_yaml = HandleYaml(CONFIG_FILE_DIR)

if __name__ == "__main__":
    do_yaml = HandleYaml(CONFIG_FILE_DIR)
    pass





