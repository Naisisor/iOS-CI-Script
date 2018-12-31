from biplist import *


class PlistOperation:
    def __init__(self, plist_path):
        self.plist_path = plist_path
        self.content = self.read()

    def read(self):
        """ 读取 plist 文件内容 """
        return readPlist(self.plist_path)

    def rewrite(self):
        """ 修改文件内容 """
        writePlist(self.content, self.plist_path, binary=False)

    def modify(self, key, val):
        """ 修改 key 的 val """
        self.content[key] = val
