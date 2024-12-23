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
  -v /media/tony/22980B44725E901B/1_Movies:/movies \
  -v /media/tony/22980B44725E901B/0_Music:/music \
  --restart unless-stopped \
docker.io/linuxserver/plex:latest

