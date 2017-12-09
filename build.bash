IMG="sebseib/nextcloud"
TAG=$1
if [ -z $TAG ]
then
 TAG="latest"
fi
docker image build -t $IMG:$TAG .
