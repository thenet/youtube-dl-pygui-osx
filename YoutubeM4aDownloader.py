from __future__ import unicode_literals
from Cocoa import *
from Foundation import NSObject
import youtube_dl
import subprocess
import os
import tempfile
import locale

class YoutubeM4aDownloaderController(NSWindowController):
    titleTextField = objc.IBOutlet()
    artistTextField = objc.IBOutlet()
    albumTextField = objc.IBOutlet()
    urlTextField = objc.IBOutlet()
    metadataProgressIndicator = objc.IBOutlet()
    downloadProgressIndicator = objc.IBOutlet()
    downloadButton = objc.IBOutlet()
   
    def windowDidLoad(self):
        NSWindowController.windowDidLoad(self)

        # Start the counter
        self.title = ""
        self.artist = ""
        self.album = ""
        #self.url="https://www.youtube.com/watch?v=sAF1Ka1ogEg"
        self.url="http://www.youtube.com/watch?v="
        self.urlTextField.setStringValue_(self.url)
        self.file= ""
        self.downloadenabled = False

        self.tempdir = tempfile.mkdtemp()
        os.chdir(os.path.join(os.getcwd(), self.tempdir))
        NSLog("tempdir:" + self.tempdir)

    @objc.IBAction
    def getMetadata_(self, sender):
        #self.count += 1
        self.metadataProgressIndicator.startAnimation_(self)
        self.url = self.urlTextField.stringValue()
        #self.randomField.setEnabled_(sender.state() == NSOnState)

        # download metadata
        ydl = youtube_dl.YoutubeDL()
        r = None
        with ydl:
            r = ydl.extract_info(self.url, download=False)  # don't download, much faster 

        # print some typical fields
        #print "%s " % (r['title'])
        titlestring = r['title']
        titlearray = titlestring.split(" - ");
        self.artist = titlearray[0];
        if len(titlearray) > 1:
            self.title = titlearray[1];
            self.album = titlearray[1] + " - Single"
        print "test"
        print "Artist: " + self.artist.encode('ascii', 'ignore').decode('ascii');
        print "Title: " + self.title.encode('ascii', 'ignore').decode('ascii');
        NSLog("Artist: " + self.artist.encode('ascii', 'ignore').decode('ascii') + " Title: " + self.title.encode('ascii', 'ignore').decode('ascii'))

        self.updateDisplay()
        #enable download button
        if self.downloadenabled == False:
            self.downloadButton.setEnabled_(sender.state() == NSOnState)
            self.downloadenabled = True
        self.metadataProgressIndicator.stopAnimation_(self)

    @objc.IBAction
    def downloadFile_(self, sender):
        #self.count -= 1
        #self.updateDisplay()
        self.downloadProgressIndicator.startAnimation_(self)

        #read gui values
        self.title = self.titleTextField.stringValue()
        self.artist = self.artistTextField.stringValue()
        self.album = self.albumTextField.stringValue() 

        def youtubedl_hook(d):
            if d['status'] == 'finished':
                print('Done downloading, now converting ...')
                print(d['filename'].encode('ascii', 'ignore').decode('ascii'))
                NSLog("Downloaded... " + d['filename'].encode('ascii', 'ignore').decode('ascii'))
                self.file = d['filename']

        ydl_opts = {
            'format': 'bestaudio/best', # choice of quality
            'extractaudio' : True,      # only keep the audio
            'progress_hooks': [youtubedl_hook],
            'outtmpl': 'file.%(ext)s'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])
        #self.file = "Lhasa de Sela - My name.m4a"
        #embed metadata
        self.embedMetadata()
        #move file to users download folder
        homepath = os.path.expanduser('~')
        NSLog(homepath)
        os.rename(self.file, homepath + "/Downloads/"+ self.title.encode('ascii', 'ignore').decode('ascii') + ".m4a")
        #reveal file
        subprocess.call(["open", "-R", homepath + "/Downloads/"+ self.title.encode('ascii', 'ignore').decode('ascii') + ".m4a"])
        self.clearFields()

        self.downloadProgressIndicator.stopAnimation_(self)

    def updateDisplay(self):
        self.titleTextField.setStringValue_(self.title)
        self.artistTextField.setStringValue_(self.artist)
        self.albumTextField.setStringValue_(self.album)
        #self.urlTextField.setStringValue_(self.url)

    def clearFields(self):
        self.title=""
        self.artist=""
        self.album=""
        self.updateDisplay()

    def embedMetadata(self):
        metaargs = ["AtomicParsley", self.tempdir+"/"+self.file,
        "--title", self.title,
        "--artist", self.artist,
        "--album", self.album,
        "--overWrite"]
        subprocess.call(metaargs)


if __name__ == "__main__":
    app = NSApplication.sharedApplication()

    #setlocale
    #locale.setlocale(locale.LC_ALL, '')
    
    # Initiate the contrller with a XIB
    viewController = YoutubeM4aDownloaderController.alloc().initWithWindowNibName_("YoutubeM4aDownloader")

    # Show the window
    viewController.showWindow_(viewController)

    # Bring app to top
    NSApp.activateIgnoringOtherApps_(True)
    
    from PyObjCTools import AppHelper
    AppHelper.runEventLoop()
