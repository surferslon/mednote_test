docker pull mongo
docker built -t mednote

docker network create mednote_network
docker run --rm -d -p 27017-27019:27017-27019 --name mongo --network mednote_network mongo --bind_ip_all
docker run --rm -d -p 8080:8080 --name aioserver --network mednote_network mednote

