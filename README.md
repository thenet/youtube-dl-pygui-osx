# youtube-dl-pygui-osx
Small GUI Python Obj-C Wrapper for youtube-dl

![Screenshot](/resources/screenshot.png)

##Requirements
* OS X
* youtube-dl
* ffmpeg
* AtomicParsley
* brew
```
easy_install youtube-dl
brew install ffmpeg
brew install AtomicParsley
```

##Build
for debug
```
python setup.py py2app
./dist/YoutubeM4aDownloader.app/Contents/MacOS/YoutubeM4aDownloader 
```
for release
```
python setup.py py2app -A
```
