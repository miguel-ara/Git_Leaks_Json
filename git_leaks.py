#! user/bin/python3

from git import Repo
import re
import signal
import sys
import json

REPO_DIR = './skale-manager'
KEY_WORDS = ['credentials', 'password', 'key', 'username']


def handler_signal(signal, frame):
    print("SALIENDO DEL PROGRAMA")
    sys.exit()


def extract(repo_dir):
    repo = Repo(repo_dir)
    dir(repo)
    commits = list(repo.iter_commits('develop'))
    return commits


def transform(commits):

    diccionario = dict()
    for i in commits:
        for word in KEY_WORDS:
            if re.search(word, i.message, re.IGNORECASE):
                key = i.hexsha
                data = i.message
                diccionario[key] = data

    return diccionario


def load(diccionario, archivo):

    with open(archivo, 'w') as file:
        json.dump(diccionario, file, indent=4)

    with open(archivo, 'r') as file:
        res = json.load(file)
        res_visual = json.dumps(res, indent=4)

    print(res_visual)


if __name__ == '__main__':

    signal.signal(signal.SIGINT, handler_signal)
    commits = extract(REPO_DIR)
    diccionario = transform(commits)
    load(diccionario, "leaks.json")
