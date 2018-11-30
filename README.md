# nextcloud-docker
## Dockerfile
### Build this image
~~~~ 
docker image build --build-arg "NC_ARCHIVE=https://download.nextcloud.com/server/releases/latest.zip" -t me/myrepo:mytag .
~~~~

### Build arguments
| environment | description | default |
|---|---|---|
| NC_ARCHIVE | full URL to download the nextcloud archive | https://download.nextcloud.com/server/releases/latest.zip |

### Environments
| environment | description | default |
|---|---|---|
| NEXTCLOUD_DB_NAME | Name of the nextcloud mysql instance | nextcloud |
| NEXTCLOUD_DB_USER | Name of the nextcloud mysql user | nextcloud |
| NEXTCLOUD_DB_PASS | Password for the nextcloud mysql user | nextcloud |
| NEXTCLOUD_ADMIN_PASS | Initial password for the nextcloud admin user | nextcloud |
| NEXTCLOUD_PUB_PROTO | Protocol used to access the nextcloud instance in public (http/https) | https |
| NEXTCLOUD_PUB_DOMAIN | URL used to access the nextcloud instance in public | nextcloud.example.com |


## Automated build (build.py):
~~~~
usage: build.py [-h] [--check] [--release RELEASE] [--no_beta] [--no_rc]
                --dockeruser DOCKERUSER [--dockerpwfile DOCKERPWFILE]
                --dockerrepo DOCKERREPO [--maxattempts MAXATTEMPTS]

optional arguments:
  -h, --help            show this help message and exit
  --check               check only
  --release RELEASE     version to build
  --no_beta             do not include beta releases (ignored when specific
                        release is defined)
  --no_rc               do not include release candidates (ignored when
                        specific release is defined)
  --dockeruser DOCKERUSER
                        username for docker login
  --dockerpwfile DOCKERPWFILE
                        file with docker password
  --dockerrepo DOCKERREPO
                        destination docker repository
  --maxattempts MAXATTEMPTS
                        max. attempts to build and push the image
~~~~
### example: build latest release without release candidates
~~~~ 
python3 build.py --release "latest" --no_rc --dockeruser sebseib --dockerpwfile .pwfile --dockerrepo "sebseib/nextcloud" 
~~~~

### example: build specific release
~~~~ 
python3 build.py --release "15.0.0beta1" --dockeruser sebseib --dockerpwfile .pwfile --dockerrepo "sebseib/nextcloud" 
~~~~
