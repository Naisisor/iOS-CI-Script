class Configuration:
    def __init__(self, params: dict, conf='Enterprise'):
        """ 初始化 plist 配置参数
        :param params
        :type dict
        :param conf iOS app build configuration name
        """
        self.app_name = params.get('appName')
        self.workspace = params.get('workspace')
        self.scheme = params.get('scheme')
        self.plist_path_list = params.get('plistPaths')
        self.icon_path = params.get('iconPath')
        self.bundle_id = params.get(conf).get('bundleID')
        self.method = params.get(conf).get('method')
        self.profiles = params.get(conf).get('provisioningProfiles')
        self.team_id = params.get(conf).get('teamID')
