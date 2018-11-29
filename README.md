# nextcloud-docker
## build.py:
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
python3 build.py --release "latest" --no_rc --dockeruser user1 --dockerpwfile .pwfile --dockerrepo "user1/nextcloud" 
~~~~
