# Project setup

## GStreamer installation for Windows

### Install MSYS2
link : https://www.msys2.org/#installation \
notes : uncheck the run msys2 now

### MSYS2 setup

Open up MSYS MINGW 64 (dont use any version beside this)

Update MSYS2 :
```
pacman -Syu
```

Install GStreamer, GstRtspServer, Python, PyGObject lib and some plugins needed in MSYS minGW 64 :
```
pacman -S mingw-w64-x86_64-gstreamer mingw-w64-x86_64-gst-devtools mingw-w64-x86_64-gst-plugins-{base,good,bad,ugly} mingw-w64-x86_64-python3 mingw-w64-x86_64-python3-gobject mingw-w64-x86_64-python3-pip mingw-w64-x86_64-gst-rtsp-server
```