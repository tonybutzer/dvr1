# Audio

## Playlists

- use plex to create - highly visual and interative
- export using web interface and python script to pick apart the ugly, complex xml
- see plex jupyter notebook for prototype code

## Enjoying

- nvlc playlist.m3u - is the best, simplist (setup is easier, playback is easier) simple way for just listening to music
    - keyboard shortcuts
	- n : next
	- a : volume up
	- z : volume down
	- r - randomize the list 

- nvlc ultimate_sample.m3u
- nvlc /tmp/Christmas.m3u

- use plex on remote computers for access in place to music library on media ssd

## Plex and Recorder

My strategy is to 
- assign one hdh box to plex i
- and one hdh to my recorders 
- using the ip address

```
(tv) tony@dopey:~$ hdhomerun_config discover
hdhomerun device 103AF69D found at 192.168.0.50
hdhomerun device 107078C9 found at 192.168.0.93
```

---
```
(tv) tony@dopey:~$ hdhomerun_config 103AF69D get /lineup/location
US:57101
```
