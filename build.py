#!/usr/bin/env python

import requests
import argparse
import json
import os

github_api = "https://api.github.com/repos/"
download_url = "https://download.nextcloud.com/server/"
download_stable = "releases"
download_pre = "prereleases"
dockerhub_api = "https://hub.docker.com/v2/"


def _parsargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="check only")
    parser.add_argument("--release", default="latest", help="version to build")
    parser.add_argument("--no_beta", action="store_true", help="do not include beta releases (ignored when specific release is defined)")
    parser.add_argument("--no_rc", action="store_true", help="do not include release candidates (ignored when specific release is defined)")
    parser.add_argument("--dockeruser", help="username for docker login", required=True)
    parser.add_argument("--dockerpwfile", default=".dockerpw", help="file with docker password")
    parser.add_argument("--dockerrepo", help="destination docker repository", required=True)
    parser.add_argument("--maxattempts", help="max. attempts to build and push the image", default=1)
    return parser.parse_args()


args = _parsargs()

def _webrequest(url):
    resp = requests.get(url)
    if not resp.status_code == 200:
        print(resp.text)
        return None
    return requests.get(url)


def _check_dockerhub_tag(owner, repo, tag):
    resp = requests.get(dockerhub_api + "repositories/" + owner + "/" + repo + "/tags/" + tag)
    if resp.status_code == 200:
        return True
    else:
        return False


def _get_nextcloud_release(version):
    tagfilter = []
    url = github_api + "nextcloud/server/tags"
    resp = _webrequest(url)

    if resp is None:
        return {}

    result = {}
    latest = None

    # always include betas & RC when release version is specified
    if version == "latest":
        if args.no_beta:
            tagfilter.append("beta")
        if args.no_rc:
            tagfilter.append("RC")

    jsn = json.loads(resp.text)
    count = 0
    for item in jsn:
        tagname = item["name"].replace('v', '')
        if tagname and (not any(flt in tagname for flt in tagfilter)):
            if count == 0:
                latest = tagname
            result[tagname] = {"version": tagname}
            count = count + 1

    if version == "latest":
        return result[latest]
    else:
        return result[args.release]


def _build_docker_image(release):
    print("BUILDING: " + str(release))
    ncurl = download_url
    dockerrepo = args.dockerrepo
    if ("beta" in release["version"]) or ("RC" in release["version"]):
        ncurl += download_pre
    else:
        ncurl += download_stable
    ncurl += "/nextcloud-" + str(release["version"]) + ".zip"

    print("download url is '" + ncurl + "'")

    if not args.check:
        os.system("docker image build --build-arg NC_ARCHIVE=" + ncurl + " -t " + dockerrepo + ":" + release["version"] + " .")
        os.system("cat " + args.dockerpwfile + " | docker login --username " + args.dockeruser + " --password-stdin")
        os.system("docker image push " + dockerrepo + ":" + release["version"])


def _main():

    if args.check:
        print("Running in CHECK mode!")

    rel = _get_nextcloud_release(args.release)
    newrel = False
    available = False
    if len(rel):
        cnt = 0
        for n in range(0, int(args.maxattempts)):
            available = _check_dockerhub_tag(args.dockeruser, args.dockerrepo.replace(args.dockeruser + '/', ''), rel["version"])

            if available:
                print("target tag " + rel["version"] + " is available on docker hub -> finished.")
                break
            else:
                newrel = True
                print("build attempt: " + str(cnt + 1) + "/" + str(args.maxattempts))
                _build_docker_image(rel)
            cnt = cnt + 1

    if newrel and available:
        print("NEW RELEASE PUBLISHED! ")


if __name__ == "__main__":
    _main()
