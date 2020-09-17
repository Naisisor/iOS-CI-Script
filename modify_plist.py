from utils.configuration import Configuration
from utils.env_enum import EnvEnum
from utils.handle_plist import HandlePlist


class ModifyPlist(HandlePlist):
    """ 修改配置文件 """

    def __init__(self, plist_path):
        """
        :param plist_path: plist 文件路径
        """
        super().__init__(plist_path)
        self.app_config = Configuration(
            self.content, conf=EnvEnum.CONFIGURATION.value)
        self.export_plist_path = f'{EnvEnum.SCRIPT_PATH.value}/plist/{self.app_config.method}.plist'
        self.icon_url = f'{EnvEnum.SCRIPT_URL.value}{self.app_config.icon_path}'

    def modify_project_plist(self):
        """ 修改项目中的需要修改的 plist 文件 """
        for plist_path in self.app_config.plist_path_list:
            plist_full_path = f'{EnvEnum.WORKSPACE.value}/{plist_path}'
            project_plist = HandlePlist(plist_full_path)
            app_name = project_plist.content.get(
                'CFBundleDisplayName')
            if EnvEnum.CONFIGURATION.value != EnvEnum.DIST_CONFIGURATION_NAME.value:
                project_plist.modify(
                    'CFBundleDisplayName',
                    f'{app_name} {EnvEnum.BUILD_NUM.value}')  # 修改 app 名称
            project_plist.modify(
                'CFBundleShortVersionString',
                EnvEnum.APP_VERSION.value)  # 修改 app 版本号
            project_plist.modify(
                'CFBundleVersion',
                EnvEnum.BUILD_NUM.value)  # 修改 ipa 构建号
            project_plist.write()

    def modify_export_plist(self):
        """ 修改 exportOptions plist 文件 """
        export_plist = HandlePlist(self.export_plist_path)
        export_plist.modify('teamID', self.app_config.team_id)
        export_plist.modify('provisioningProfiles', self.app_config.profiles)
        export_plist.write()

    def modify_services_plist(self):
        # 修改 itms-services.plist
        service = HandlePlist(
            f'{EnvEnum.SCRIPT_ITMS_SERVICE_PATH.value}')
        assets = service.content['items'][0]['assets']
        assets[0]['url'] = f'{EnvEnum.ARCHIVE_URL_HTTPS.value}{self.app_config.scheme}.ipa'
        assets[1]['url'] = self.icon_url
        assets[2]['url'] = self.icon_url
        metadata = service.content['items'][0]['metadata']
        metadata['bundle-identifier'] = self.app_config.bundle_id
        metadata['bundle-version'] = EnvEnum.APP_VERSION.value
        metadata['title'] = self.app_config.app_name
        service.write()
