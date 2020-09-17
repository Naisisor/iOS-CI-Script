import plistlib


class HandlePlist:
    def __init__(self, path):
        self.path = path
        self.content = self.read()

    def read(self):
        """ 读取 plist 文件内容 """
        with open(self.path, mode='rb') as f:
            return plistlib.load(f)

    def write(self):
        """ 修改文件内容 """
        with open(self.path, mode='wb') as f:
            plistlib.dump(self.content, f)

    def modify(self, key, val):
        """ 修改 key 的 val """
        self.content[key] = val
