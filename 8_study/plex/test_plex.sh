docker kill plex
docker rm plex
docker run -d \
  --name=plex \
  --net=host \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Etc/UTC \
  -e VERSION=docker \
  -e PLEX_CLAIM= `#optional` \
  -v /path/to/plex/library:/config \
  -v /path/to/tvseries:/tv \
  --restart unless-stopped \
docker.io/linuxserver/plex:latest

#/media/tony/mediabackup1/9_plex_backup/

