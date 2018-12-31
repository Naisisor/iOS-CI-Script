from bs4 import BeautifulSoup


class HTMLTools:
    def __init__(self):
        pass

    @staticmethod
    def read_html(path):
        """读取 html 文件内容
        :param path html 文件的路径
        """
        with open(path, encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def parse_html(content):
        """ 解析 html 内容 """
        soup = BeautifulSoup(content, "html.parser")
        return soup
