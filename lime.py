import os
import eyed3
import spotipy
import magic
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fdia
from spotipy.oauth2 import SpotifyClientCredentials

client_id = "[REDACTED]"
client_secret = "[REDACTED]"

client_credentials_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class MainWindow(ttk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pack()
        
        self.create_widgets()
        
    def create_widgets(self):
        self.library = ""
                                           #DIRECTORY LABEL
        self.lbl_currentdir = ttk.Label(   self,
                                           text       = self.library)
        self.lbl_currentdir.grid(          row        = 0,
                                           column     = 1,
                                           rowspan    = 1,
                                           columnspan = 1,
                                           sticky     = "W")
        
                                           #CHOOSE FOLDER BUTTON
        self.btn_choosefolder = ttk.Button(self,
                                           text       = "CHOOSE FOLDER",
                                           command    = self.get_library)
        self.btn_choosefolder.grid(        row        = 1,
                                           column     = 1,
                                           rowspan    = 1,
                                           columnspan = 1,
                                           sticky     = "WENS")
                                           
                                           #BULK CHANGE BUTTON
        self.btn_bulkchange = ttk.Button(  self,
                                           text       = "BULK CHANGE",
                                           command    = self.change_tags)
        self.btn_bulkchange.grid(          row        = 0,
                                           column     = 2,
                                           rowspan    = 2,
                                           columnspan = 1,
                                           sticky     = "WENS")
                                           
                                           #UD ARTIST LABEL
        self.lbl_ud_artist = ttk.Label(    self,
                                           text       = "USER-DEFINED ARTIST:")
        self.lbl_ud_artist.grid(           row        = 0,
                                           column     = 0,
                                           rowspan    = 1,
                                           columnspan = 1,
                                           sticky = "W")
                                            
                                           #UD ARTIST ENTRY
        self.entry_ud_artist = ttk.Entry(  self)
        self.entry_ud_artist.grid(         row = 1,
                                           column = 0,
                                           rowspan = 1,
                                           columnspan = 1,
                                           sticky = "WENS")
       
        self.tag_cols = ("current_tags", "suggested_tags")
                                            
                                           #RESULTS TREEVIEW
        self.tv_results = ttk.Treeview(    self, 
                                           columns    = self.tag_cols)
       
        self.tv_results.heading(           column     = "#0", 
                                           text       = "Song") 
                                           
        self.tv_results.heading(           column     = "current_tags", 
                                           text       = "Current Tags") 
                                           
        self.tv_results.heading(           column     = "suggested_tags", 
                                           text       = "Suggested Tags")
                                           
        self.tv_results.grid(              row        = 2,
                                           column     = 0,
                                           rowspan    = 1,
                                           columnspan = 3,
                                           ipadx      = 300,
                                           ipady      = 200,
                                           sticky     = "WENS")
       
       
        
    def get_library(self):
        # allow the user to pick a directory
        self.library = tk.filedialog.askdirectory().replace("/", "\\")
        self.lbl_currentdir["text"] = "Library - " + self.library
        
        joiner = "; "
        self.tv_results.delete(*self.tv_results.get_children())
        print("GETTING MUSIC FROM LIBRARY")
        
        # add contents of selected folder to the treeview
        for item in os.listdir(self.library):
            if ".mp3" in item:
                itempath = self.library + "\\" + item
                
                message = "Getting Metadata for: {0}".format(itempath)
                print(message)
                
                song_data_str = "ARTIST: {0}; TITLE: {1}; ALBUM: {2}, TRACK#: {3}"
                current_tags = self.get_curr_tags(itempath)
                current_tags_str = song_data_str.format(current_tags["artist"], current_tags["title"], current_tags["album"], current_tags["tracknum"])
                
                song_data_str = "ARTIST: {0}; TITLE: {1}; ALBUM: {2}, TRACK#: {3}"
                suggested_tags = self.get_sugg_tags(item, itempath)
                suggested_tags_str = song_data_str.format(suggested_tags["artist"], suggested_tags["title"], suggested_tags["album"], suggested_tags["tracknum"])
                
                self.tv_results.insert("", "end", text = item, values = (current_tags_str, suggested_tags_str))
                
    def get_curr_tags(self, songpath):
        song = eyed3.load(songpath)
        
        # checks if the song even has tags
        # if not, makes all tags empty strings, as opposed to NoneType
        if song.tag is not None:
            song_artist = song.tag.artist
            song_title = song.tag.title
            song_album = song.tag.album    
            song_tracknum = song.tag.track_num[0]
        else:
            song_artist = ""
            song_title = ""
            song_album = ""
            song_tracknum = ""
            
        song_data = {
                        "artist"   : song_artist,
                        "title"    : song_title,
                        "album"    : song_album,
                        "tracknum" : song_tracknum
                    }
        
        return song_data
        
    def get_sugg_tags(self, song_filename, songpath):
        song_udartist = self.entry_ud_artist.get()
        song_filename = song_filename.replace(".mp3", "")
        song = eyed3.load(songpath)
        
        # checks if the song even has tags
        # if not, makes all tags empty strings, as opposed to NoneType
        if song.tag is not None:
            song_artist = song.tag.artist
            song_title = song.tag.title
            song_album = song.tag.album    
            song_tracknum = song.tag.track_num[0]
        else:
            song_artist = ""
            song_title = ""
            song_album = ""
            song_tracknum = ""
        
        # bases the query on whether you have certain parameters
        # or not
        if song_artist + song_title != "":
            q = "{0} {1}".format(song_artist, song_title)
        
        elif song_artist != "" and song_title == "":
            q = "{0} {1}".format(song_artist, song_filename)
            
        elif song_artist == "" and song_title != "":
            q = "{0} {1}".format(song_udartist, song_title) # uses a user-defined artist to increase accuracy of results
        
        # the most likely condition, considering the user resorted to using this app.
        elif song_artist == "" and song_title == "": 
            q = "{0} {1}".format(song_udartist, song_filename) # again, uses that user-defined artist
            
            
        results = sp.search(q=q) 
        
        try:    song_artist = results["tracks"]["items"][0]["artists"][0]["name"]
        except: song_artist = "N/A"
        
        try:    song_title = results["tracks"]["items"][0]["name"]
        except: song_title = "N/A"
        
        try:    song_album = results["tracks"]["items"][0]["album"]["name"]
        except: song_album = "N/A"
        
        try:    song_tracknum = results["tracks"]["items"][0]["track_number"]
        except: song_album = "N/A"
        
        song_data = {
                        "artist"   : song_artist,
                        "title"    : song_title,
                        "album"    : song_album,
                        "tracknum" : song_tracknum
                    }

        return song_data
        
    def change_tags(self):
        print("CHANGING METADATA")

        
        for item in os.listdir(self.library):
            if ".mp3" in item:
                itempath = self.library + "\\" + item
                suggested_tags = self.get_sugg_tags(item, itempath)
                
                song = eyed3.load(itempath)
                song.initTag()
                
                print("CHANGING metadata for:", itempath)
                song.tag.artist = suggested_tags["artist"]
                song.tag.title = suggested_tags["title"]
                song.tag.album = suggested_tags["album"]
                song.tag.tracknum = suggested_tags["tracknum"]
                song.tag.save()
                print("CHANGED metadata for:", itempath)
                
root = tk.Tk()
root.title("LIME 0.1")
app = MainWindow(parent=root)
app.mainloop()
