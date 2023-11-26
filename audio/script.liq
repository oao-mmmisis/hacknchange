#!/usr/bin/liquidsoap

settings.init.allow_root.set(true)

output.icecast(%vorbis, host="icecast2", port=8000, password="chael7Ai", mount="dante", single("/music/dante.ogg"))
output.icecast(%vorbis, host="icecast2", port=8000, password="chael7Ai", mount="ele", single("/music/ele.ogg"))
output.icecast(%vorbis, host="icecast2", port=8000, password="chael7Ai", mount="cre", single("/music/cre.ogg"))
