"""GitHub CLI(ghコマンド)で、自分のリポジトリ、自分の所属している組織のリポジトリを全取得する"""

import os
import json
import datetime
import subprocess

BASE_PATH = "/home/user-hoge/github-backup"
IS_CLONE_ORGS_REPOS = True


def exec_cmd(cmds):
    """コマンドを実行する"""
    return subprocess.run(
        cmds, shell=False, check=True, capture_output=True, text=True
    ).stdout


def json_to_pyobj(json_str):
    """jsonをpythonのlist/dictに変換する"""
    return json.loads(json_str)


def get_user_name():
    """ログインしているユーザ名を取得する"""
    return exec_cmd(["gh", "api", "user", "--jq", ".login"]).strip()


def get_user_orgs():
    """ユーザの所属している組織を調べる"""
    json_data = exec_cmd(["gh", "api", "user/orgs"])
    return [i["login"] for i in json_to_pyobj(json_data)]


def get_repos_list(owner_name):
    """ユーザーor組織のリポジトリのリストを取得"""
    json_data = exec_cmd(["gh", "repo", "list", owner_name, "--json", "name"])
    return [i["name"] for i in json_to_pyobj(json_data)]


def get_nowtime():
    return datetime.datetime.now().isoformat().replace(":", "-")


def mk_and_cd_dir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    os.chdir(path)


if __name__ == "__main__":
    mk_and_cd_dir(BASE_PATH)
    mk_and_cd_dir(get_nowtime())
    owners = []
    owners.append(get_user_name())
    if IS_CLONE_ORGS_REPOS:
        owners.extend(get_user_orgs())
    for owner in owners:
        mk_and_cd_dir(owner)
        for repo in get_repos_list(owner):
            exec_cmd(["gh", "repo", "clone", f"{owner}/{repo}"])
        mk_and_cd_dir("..")
