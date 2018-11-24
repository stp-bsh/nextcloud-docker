import requests
import argparse
import json
import os

github_api = "https://api.github.com/repos/"
download_url = "https://download.nextcloud.com/server/"
download_stable = "releases"
download_pre = "prereleases"
destimg = "sebseib/nextcloud"


def _parsargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="check only")
    parser.add_argument("--release", default="latest")
    parser.add_argument("--beta", action="store_true")
    parser.add_argument("--rc", action="store_true")
    parser.add_argument("--dockerpwfile", default=".dockerpw")
    return parser.parse_args()

args = _parsargs()


def _read_dockerpw():
    with open(args.dockerpwfile) as file:
        return file.read()


def _webrequest(url):
    resp = requests.get(url)
    if not resp.status_code == 200:
        print(resp.text)
        return None
    return requests.get(url)


def _get_nextcloud_release(version):
    tagfilter = []
    url = github_api + "nextcloud/server/tags"
    resp = _webrequest(url)

    if resp == None:
        return {}

    result = {}
    latest = None

    # always include betas & RC when release version is specified
    if args.release == "latest":
        if not args.beta:
            tagfilter.append("beta")
        if not args.rc:
            tagfilter.append("RC")

    jsn = json.loads(resp.text)
    count = 0
    for item in jsn:
        tagname = item["name"].replace('v', '')
        if tagname and (not any(flt in tagname for flt in tagfilter)):
            if count == 0:
                latest = tagname
            result[tagname] = {"version": tagname }
            count = count + 1

    if version == "latest":
        return result[latest]
    else:
        return result[args.release]


def _build_docker_image(release):
    print("BUILDING: " + str(release))
    ncurl = download_url
    dockerpw = _read_dockerpw()
    if ("beta" in release["version"]) or ("RC" in release["version"]):
        ncurl += download_pre
    else:
        ncurl += download_stable
    ncurl += "/nextcloud-" + str(release["version"]) + ".zip"

    print("download url is '" + ncurl + "'")

    if not args.check:
        os.system("docker image build --build-arg NC_ARCHIVE=" + ncurl + "-t sebseib/nextcloud:" + release["version"] + " .")
        os.system("echo " + dockerpw + " | docker image push " + destimg + ":" + release["version"])


def _main():
    if args.check:
        print("Running in CHECK mode!")

    rel = _get_nextcloud_release(args.release)

    if len(rel):
        _build_docker_image(rel)


if __name__ == "__main__":
    _main()
