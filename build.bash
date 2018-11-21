IMG="sebseib/nextcloud"
TAG=$1
if [ -z $TAG ]
then
 TAG="latest"
fi
export NC_VERSION=${TAG}
docker image build --build-arg NC_VERSION=${TAG} -t $IMG:$TAG .
DOCKERPW=$(cat ~/.dockerpw) 
echo $DOCKERPW | docker login --username sebseib --password-stdin
docker image push ${IMG}:${TAG}
git tag -a ${TAG} -m ${TAG}
git push --tags
