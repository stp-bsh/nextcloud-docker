import requests
import json
import argparse
import os
import subprocess


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--beta", default="no")
    parser.add_argument("--rc", default="no")
    return parser.parse_args()


def _get_github_releases_or_tags(owner, repo, type, beta=False, rc=False):
    github_api = "https://api.github.com/repos/" + owner + "/" + repo + "/" + type;
    tagfilter = []
    result = []

    if not beta:
        tagfilter.append("beta")
    if not rc == "yes":
        tagfilter.append("RC")

    resp = requests.get(github_api)
    if resp.status_code == 200:
        jresp = json.loads(resp.text)
        for tag in jresp:
            name = tag["name"]
            if name and (not any(flt in name for flt in tagfilter)):
                result.append(name)

    return result


def _main():
    args = _parse_args()
    nextcloud_versions_github = _get_github_releases_or_tags("nextcloud", "server", "tags", args.beta == "yes", args.rc == "yes")
    nextcloud_versions_own = _get_github_releases_or_tags("sebseib", "nextcloud-docker", "tags", args.beta == "yes", args.rc == "yes")

    buildq = []

    for version in nextcloud_versions_github:
        v = version.replace('v', '')
        if not (v in nextcloud_versions_own):
            buildq.append(v)

    if len(buildq) == 0:
        print("There are no new nextcloud versions to build!")
    else:
        print("available nextcloud version on github: " + str(nextcloud_versions_github))
        print("own nextcloud version available: " + str(nextcloud_versions_own))
        print("nextcloud versions to build: " + str(buildq))

        for item in buildq:
            print("===> BUILDING VERSION " + item)
            subprocess.call(["git", "pull", "origin", "master"])
            os.system("./build.bash " + item)


if __name__ == "__main__":
    _main()