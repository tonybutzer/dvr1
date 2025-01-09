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
  -v /media/tony/plexLive/plexroot/1_Movies:/movies \
  -v /media/tony/plexLive/plexroot/0_Music:/music \
  -v /media/tony/plexLive/plexroot/2_Audiobooks:/audiobooks \
  --restart unless-stopped \
docker.io/linuxserver/plex:latest

#/media/tony/mediabackup1/9_plex_backup/

