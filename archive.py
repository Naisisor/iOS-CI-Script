import os
import shutil
import subprocess

from utils.env_enum import EnvEnum
from utils.make_qr_code import make_qr


def upload_itunes_connect(ipa_path):
    """ 上传 iTunes Connect """
    if EnvEnum.ITC_USER.value is None \
            or EnvEnum.ITC_PASSWORD.value is None:
        raise Exception('开发者账号用户名和密码不能为空')
    subprocess.run('echo "Validating app ..."', shell=True)
    subprocess.run(f'time {EnvEnum.ALTOOL.value} '
                   f'--validate-app '
                   f'-f {ipa_path} '
                   f'-u {EnvEnum.ITC_USER.value} '
                   f'-p {EnvEnum.ITC_PASSWORD.value}', shell=True)
    subprocess.run('echo "Uploading app to iTunes Connect ..."', shell=True)
    subprocess.run(f'time {EnvEnum.ALTOOL.value} '
                   f'--upload-app '
                   f'-f {ipa_path} '
                   f'-u {EnvEnum.ITC_USER.value} '
                   f'-p {EnvEnum.ITC_PASSWORD.value}', shell=True)


def archive_file(scheme, app_name, icon_path, icon_url):
    """ 处理需要归档的文件 """
    if os.path.exists(EnvEnum.ARCHIVE_PATH.value):
        shutil.rmtree(EnvEnum.ARCHIVE_PATH.value)
    os.mkdir(EnvEnum.ARCHIVE_PATH.value)

    # copy 文件
    archive_ipa_path = f'{EnvEnum.ARCHIVE_PATH.value}/{scheme}.ipa'
    shutil.copy(f'{EnvEnum.BUILD_PATH.value}/{scheme}/{scheme}.ipa',
                archive_ipa_path)
    shutil.copy(f'{EnvEnum.SCRIPT_ITMS_SERVICE_PATH.value}',
                f'{EnvEnum.ARCHIVE_PATH.value}/{scheme}.plist')

    # dSYM 文件处理
    dsym_zip = f'{EnvEnum.BUILD_PATH.value}/{scheme}.dsym.zip'
    if os.path.exists(dsym_zip):
        shutil.copy(
            dsym_zip, f'{EnvEnum.ARCHIVE_PATH.value}/{scheme}.dsym.zip')

    # 修改 html 内容
    icon_url = icon_url.replace('/', r'\/')
    build_url = EnvEnum.BUILD_URL_HTTPS.value.replace('/', r'\/')

    shutil.copy(
        f'{EnvEnum.SCRIPT_PATH.value}/static/html/download.html',
        f'{EnvEnum.ARCHIVE_PATH.value}/{scheme}.html')

    subprocess.run(
        f'sed -i "" "s/ICON_URL/{icon_url}/g" {EnvEnum.ARCHIVE_PATH.value}/{scheme}.html',
        shell=True)
    subprocess.run(
        f'sed -i "" "s/APP_NAME/{app_name}/g" {EnvEnum.ARCHIVE_PATH.value}/{scheme}.html',
        shell=True)
    subprocess.run(
        f'sed -i "" "s/BUILD_URL/{build_url}/g" {EnvEnum.ARCHIVE_PATH.value}/{scheme}.html',
        shell=True)

    # 生成二维码
    html_url = f'{EnvEnum.ARCHIVE_URL.value}{scheme}.html'
    make_qr(
        html_url,
        f'{EnvEnum.SCRIPT_PATH.value}/{icon_path}',
        f'{EnvEnum.ARCHIVE_PATH.value}/{scheme}_iOS_{EnvEnum.BUILD_NUM.value}.png')

    # 上传 iTunes Connect
    if EnvEnum.CONFIGURATION.value == EnvEnum.DIST_CONFIGURATION_NAME.value \
            and EnvEnum.UPLOAD_ITUNES_CONNECT.value == 'true':
        upload_itunes_connect(ipa_path=archive_ipa_path)
