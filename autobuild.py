import requests
import json
import argparse
import os

nc_download_url = "https://download.nextcloud.com/server/"
nc_path_stable = "releases"
nc_path_pre = "prereleases"


def _args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--beta", action="store_true", help="include beta releases")
    parser.add_argument("--rc", action="store_true", help="include release candidates")
    parser.add_argument("--check", action="store_true", help="check only")
    parser.add_argument("--dockerpwfile", default=".dockerpw")
    return parser.parse_args()

args = _args()

def _get_github_releases_or_tags(owner, repo, type, beta=False, rc=False):
    github_api = "https://api.github.com/repos/" + owner + "/" + repo + "/" + type
    tagfilter = []
    result = []

    if not beta:
        tagfilter.append("beta")
    if not rc:
        tagfilter.append("RC")

    resp = requests.get(github_api)
    if resp.status_code == 200:
        jresp = json.loads(resp.text)
        for tag in jresp:
            name = tag["name"]
            if name and (not any(flt in name for flt in tagfilter)):
                result.append(name)
    else:
        print(resp.text)

    return result


def _download_nc_release(version):
    ncdownloadurl = ""
    dest_arch = "./nextcloud.zip"

    if ("beta" in version) or ("RC" in version):
        ncdownloadurl = nc_download_url + nc_path_pre
    else:
        ncdownloadurl = nc_download_url + nc_path_stable

    full_url = ncdownloadurl + "/nextcloud-" + version + ".zip"
    print("downloading:" + full_url)
    if os.path.exists(dest_arch):
        os.remove(dest_arch)

    if not args.check:
        r = requests.get(full_url)
        with open(dest_arch, "wb") as cnt:
            cnt.write(r.content)


def _read_dockerpw():
    with open(args.dockerpwfile, 'r') as file:
        return file.read()


def _build_docker_image(tag):
    dockerpw = _read_dockerpw()
    img = "sebseib/nextcloud:" + tag
    print("building docker image: " + img)

    if not args().check:
        os.system("docker image build -t " + img + " .")
        os.system("echo " + dockerpw + " | docker login --username sebseib --password-stdin")
        os.system("docker image push " + img)
        os.system("git tag -f -a " + tag + " -m " + tag)
        os.system("git push -f --tags")


def _main():

    if args.check:
        print("!!! RUNNING IN CHECK MODE !!!")

    nextcloud_versions_github = _get_github_releases_or_tags("nextcloud", "server", "tags", args.beta, args.rc)
    nextcloud_versions_own = _get_github_releases_or_tags("sebseib", "nextcloud-docker", "tags", args.beta, args.rc)

    buildq = []

    for version in nextcloud_versions_github:
        v = version.replace('v', '')
        if not (v in nextcloud_versions_own):
            buildq.append(v)

    print("available nextcloud version on github: " + str(nextcloud_versions_github))
    print("own nextcloud version available: " + str(nextcloud_versions_own))

    if len(buildq) == 0:
        print("There are no new nextcloud versions to build!")
    else:
        print("nextcloud versions to build: " + str(buildq))

        for item in buildq:
            _download_nc_release(item)
            _build_docker_image(item)


if __name__ == "__main__":
    _main()
