import os
import subprocess

from utils.env_enum import EnvEnum


def compile_app(app_workspace, app_scheme, method):
    export_plist_path = f'{EnvEnum.SCRIPT_PATH.value}/plist/{method}.plist'

    # clean
    subprocess.run(
        f'xcodebuild clean '
        f'-workspace {app_workspace} '
        f'-scheme {app_scheme} '
        f'-configuration {EnvEnum.CONFIGURATION.value} | xcpretty -s',
        shell=True)

    # archive
    subprocess.run(
        f'xcodebuild archive '
        f'-workspace {app_workspace} '
        f'-scheme {app_scheme} '
        f'-configuration {EnvEnum.CONFIGURATION.value} '
        f'-archivePath {EnvEnum.BUILD_PATH.value}/{app_scheme} | xcpretty -s',
        shell=True)

    # export ipa
    xc_archive_file = f'{EnvEnum.BUILD_PATH.value}/{app_scheme}.xcarchive'
    if not os.path.exists(xc_archive_file):
        raise Exception(f'{app_scheme}.xcarchive 不存在，编译失败，请联系开发人员')
    subprocess.run(
        f'xcodebuild -exportArchive '
        f'-archivePath {xc_archive_file} '
        f'-exportPath {EnvEnum.BUILD_PATH.value}/{app_scheme} '
        f'-exportOptionsPlist {export_plist_path}',
        shell=True)

    # 压缩符号表
    dsym_file = f'{EnvEnum.BUILD_PATH.value}/{app_scheme}.xcarchive/dSYMs/{app_scheme}.app.dSYM'
    if os.path.exists(dsym_file):
        subprocess.call(
            f'zip -r {EnvEnum.BUILD_PATH.value}/{app_scheme}.dsym.zip {dsym_file}',
            shell=True)
