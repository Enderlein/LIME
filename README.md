# LIME
Library Metadata Enhancement Tool

# Purpose
Given an artist's name and a local music library, this program will attempt to apply accurate artist, track number, song name, and album name to each of the songs in the library according to Spotify's music database

Currently, the only available version is v0.1

Whenever I get some free time, I'll work on improving the UI and the speed of the program (it works fairly slow right now)

# How to Install
1. Download all files.
2. Open your command line in the directory you downloaded LIME to.
3. Use the following command - 
```bash
pip install -r requirements.txt
```
4. Get and set Client ID and Client Secret.

# How to get and set Client ID and Client Secret
1. Go [here](https://beta.developer.spotify.com/dashboard/applications/).
2. Create a new application.
3. Voila. You have your Client ID and Client Secret.
4. Go to the directory you downloaded LIME to.
5. Open config.py with your preferred text editor.
6. Put the Client ID in between the corresponding quotation marks.
7. Put the Client Secret in between the corresponding quotation marks.
8. Save the file.

How it should look when you're done:
```Python
client_id = "124011awbqqk8ht4oeogq065d6t7496y"
client_secret = "u5nejcrloc4b6q4cr8o8njrlvad2ce8c"
```
