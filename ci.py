from archive import archive_file
from compile import compile_app
from utils.env_enum import EnvEnum
from modify_plist import ModifyPlist


def main():
    conf_plist = ModifyPlist(EnvEnum.CONF_FILE_PATH.value)

    # 修改项目需要修改的 plist 文件
    conf_plist.modify_project_plist()

    # 修改 exportOption plist 文件
    conf_plist.modify_export_plist()

    # 修改 itms-services plist 文件
    conf_plist.modify_services_plist()

    # clean、archive、export—ipa、压缩 dSYM 文件
    compile_app(
        app_workspace=conf_plist.app_config.workspace,
        app_scheme=conf_plist.app_config.scheme,
        method=conf_plist.app_config.method)

    # 归档文件
    archive_file(
        scheme=conf_plist.app_config.scheme,
        app_name=conf_plist.app_config.app_name,
        icon_path=conf_plist.app_config.icon_path,
        icon_url=conf_plist.icon_url)


if __name__ == '__main__':
    main()
