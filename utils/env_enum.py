import os
from enum import Enum


class EnvEnum(Enum):
    # 需手动更改的参数（选择默认也可以）
    DIST_CONFIGURATION_NAME = 'Release'  # 项目工程中发布的 configuration 的名称
    ARCHIVE_DIR_NAME = 'Products'  # 归档的目录名称
    SCRIPT_DIR_NAME = 'scripts'  # 存放脚本项目的目录名称

    # 自定义环境变量
    CONF_FILE_NAME = os.getenv('CONF_FILE_NAME')  # 配置文件的名称
    CONFIGURATION = os.getenv('CONFIGURATIONS')  # app configuration
    APP_VERSION = os.getenv('APP_VERSION')  # app 版本号
    WORKSPACE_URL = os.getenv('WORKSPACE_URL')  # 工作空间 URL，需从 Jenkins 上获取 workspace url

    # iTunes Connect 配置
    UPLOAD_ITUNES_CONNECT = os.getenv('UPLOAD_ITUNES_CONNECT', 'false')  # 上传 iTunes Connect，默认 false
    ITC_USER = os.getenv('ITC_USER', None)  # 开发者账号
    ITC_PASSWORD = os.getenv('ITC_PASSWORD', None)  # 开发者密码（若开发者账号开启双重认证请使用专用密码）

    # Jenkins 环境变量
    JENKINS_URL = os.getenv('JENKINS_URL')
    JOB_URL = os.getenv('JOB_URL')
    BUILD_URL = os.getenv('BUILD_URL')

    WORKSPACE = os.getenv('WORKSPACE')
    JOB_NAME = os.getenv('JOB_NAME')
    BUILD_NUM = os.getenv('BUILD_NUMBER')

    # 路径
    BUILD_PATH = f'{WORKSPACE}/build'  # xcarchive 文件存放的路径
    SCRIPT_PATH = f'{WORKSPACE}/{SCRIPT_DIR_NAME}'  # 打包脚本存放的路径
    ARCHIVE_PATH = f'{WORKSPACE}/{ARCHIVE_DIR_NAME}'  # 归档目录的路径
    CONF_FILE_PATH = f'{SCRIPT_PATH}/configurations/{CONF_FILE_NAME}.plist'  # 配置文件存放的路径
    SCRIPT_ITMS_SERVICE_PATH = f'{SCRIPT_PATH}/plist/itms-services.plist'  # 脚本中的 itms-services.plist 的路径

    # URL
    SCRIPT_URL = f'{WORKSPACE_URL}{SCRIPT_DIR_NAME}/'  # 每次构建脚本文件的 URL
    ARTIFACT_URL = f'{BUILD_URL}artifact/'  # artifact URL
    ARCHIVE_URL = f'{ARTIFACT_URL}{ARCHIVE_DIR_NAME}/'  # 每次构建归档文件的 URL

    # HTTPS URL
    JENKINS_URL_HTTPS = os.getenv('JENKINS_URL_HTTPS') or JENKINS_URL  # 必须配置可信的 HTTPS 证书
    BUILD_URL_HTTPS = f'{JENKINS_URL_HTTPS}job/{JOB_NAME}/{BUILD_NUM}/'
    ARTIFACT_URL_HTTPS = f'{BUILD_URL_HTTPS}artifact/'  # 归档 URL
    ARCHIVE_URL_HTTPS = f'{ARTIFACT_URL_HTTPS}{ARCHIVE_DIR_NAME}/'  # 每次构建归档文件的 URL
    ARCHIVE_ITMS_SERVICE_URL = f'{ARCHIVE_URL_HTTPS}itms-services.plist'  # itms-services.plist 文件 URL

    # Command
    ALTOOL = 'xcrun altool'
