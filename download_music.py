import os
import requests
import re
from tqdm import tqdm
from mutagen.flac import FLAC,Picture
from pydub import AudioSegment

#function to get song and lyrics
def get_song(albumurl):
    try:
        response = requests.get(albumurl,stream=True)
        response.raise_for_status()
        data=response.json()
        songs = data['data']['songs']
        albumname = data['data']['name']
        coverimgurl = data['data']['coverUrl']
        albumname = albumname.replace(" ","_")
        for song in songs:
            print(song['cid'])
            url="https://monster-siren.hypergryph.com/api/song/"+song['cid']+""
            if not os.path.exists(albumname):
             if not os.path.exists(albumname):
                    os.makedirs(albumname)
             else:
                    print("Album already exists")
                    exit()
            if not os.path.exists(albumname+"/lyrcs"):
                os.makedirs(albumname+"/lyrcs")
            download(url,albumname,coverimgurl)
    except requests.exceptions.HTTPError as err:
        print("Error: ", err)
        exit()

#function to download song and lyrics
def download(url,albumname,coverimgurl):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        data=response.json()
        file_name= data['data']['name']
        songurl= data['data']['sourceUrl']
        artists = data['data']['artists']
        temp="temp.wav"
        checkmp3 = songurl.split('.')[-1][-3:]
        if checkmp3 == "mp3":
         file_name_wav_mp3=file_name+".flac"
        elif checkmp3 == "wav":
         file_name_wav_mp3=file_name+".flac"
        #get cover image
        if not os.path.exists(albumname+"/"+"cover.jpg"):
            download_cover_img= requests.get(coverimgurl, stream=True,timeout=5)
            if download_cover_img.status_code == 200:
                print("Cover image found")
            # Get the total file size for the cover image
            total_size = int(download_cover_img.headers.get('content-length', 0))
            # Download the cover image with progress bar
            with open(os.path.join(albumname,"cover.jpg"), 'wb') as f, tqdm(
                desc="Downloading cover image",
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in download_cover_img.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))
            coverimg = albumname+"/cover.jpg"
        #get song
        dwnsong= requests.get(songurl, stream=True,timeout=5)
        if dwnsong.status_code == 200:
            print("Song found: "+file_name)
        # Get the total file size for the song
        total_size = int(dwnsong.headers.get('content-length', 0))
        if os.path.exists(os.path.join(albumname,temp)):
            os.remove(albumname+"/"+temp)
            return
        # Download the song with progress bar
        with open(os.path.join(albumname,temp), 'wb') as f, tqdm(
            desc="Downloading song",
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in dwnsong.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    bar.update(len(chunk))
        if os.path.exists(albumname+"/"+file_name_wav_mp3):
            os.remove(albumname+"/"+file_name_wav_mp3)
        os.rename(os.path.join(albumname,temp), albumname+"/"+file_name_wav_mp3)
        if checkmp3 == "wav":
            print("Converting to flac")
            song = AudioSegment.from_wav(albumname+"/"+file_name_wav_mp3)
            song.export(albumname+"/"+file_name_wav_mp3,format = "flac")
        if checkmp3 == "mp3":
            print("Converting to flac")
            song = AudioSegment.from_mp3(albumname+"/"+file_name_wav_mp3)
            song.export(albumname+"/"+file_name_wav_mp3,format = "flac")
        print("Song downloaded")
        #get lyrics url
        lrcurl = data['data']['lyricUrl']
        if lrcurl is None:
            print("No lyrics found")
            add_info_to_flac(file_name_wav_mp3,artists,albumname)
            return
        else:
            print("Lyrics found")
            dwnlrc= requests.get(lrcurl, stream=True,timeout=5)
            lrc = file_name+".lrc"
            # Get the total file size for lyrics
            total_size = int(dwnlrc.headers.get('content-length', 0))
            # Download the lyrics with progress bar
            with open(os.path.join(albumname+"/lyrcs",lrc), 'wb') as f, tqdm(
                desc="Downloading lyrics",
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in dwnlrc.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))
            remove_last_digit_from_milliseconds(os.path.join(albumname+"/lyrcs",lrc), os.path.join(albumname+"/lyrcs",lrc))
            add_lyrics_to_flac(file_name_wav_mp3,lrc,artists,albumname,coverimg)
    except requests.exceptions.RequestException as e:
        #stop the program when get status code 404
        if response.status_code == 404:
         print("finished", response.status_code)
         exit()
        print("Error: ", e)

#function to add lyrics to the song that is in wav format
def add_lyrics_to_flac(file_name_wav_mp3, lrc,artists,albumname,coverimg):
    # Load the WAV file
    audio = FLAC(os.path.join(albumname,file_name_wav_mp3))
    # Add lyrics flac
    with open(os.path.join(albumname+"/lyrcs",lrc), 'r', encoding='utf-8') as lrc:
        lrc = lrc.read()
    audio['artist'] = artists
    audio['lyrics'] = lrc
    audio['title'] = file_name_wav_mp3.strip(".flac")
    audio['album'] = albumname
    # Add cover image
    if coverimg:
        image = Picture()
        with open(coverimg, 'rb') as img_file:
            image.data = img_file.read()
        image.type = 3  # Cover (front)
        image.mime = "image/jpeg"  # or image/png
        audio.add_picture(image)
    # Save the changes
    audio.save()
    print("Lyrics added to the song")

def add_info_to_flac(file_name_wav_mp3,artists,albumname):
    # Load the WAV file
    audio = FLAC(os.path.join(albumname,file_name_wav_mp3))
    audio['artist'] = artists
    audio['title'] = file_name_wav_mp3.strip(".flac")
    audio['album'] = albumname
    # Save the changes
    audio.save()

# Remove the last digit from the milliseconds in the timestamps of the lyrics
def remove_last_digit_from_milliseconds(lrc_file_path, output_file_path):
    with open(lrc_file_path, 'r', encoding='utf-8') as file:
        lyrics = file.readlines()
    # Regular expression to match the timestamp and capture the first two digits of milliseconds
    timestamp_pattern = re.compile(r'\[(\d{2}:\d{2}\.\d{2})\d\]')
    # Remove the last digit from the milliseconds in the timestamps
    cleaned_lyrics = [timestamp_pattern.sub(r'[\1]', line) for line in lyrics]
    # Write the cleaned lyrics to a new file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(''.join(cleaned_lyrics))
#main
url=input("Enter the number of the albums(divided by ','): ")
url = url.split(",")
url = [x.strip() for x in url]
for i in range(len(url)):
     albumurl = "https://monster-siren.hypergryph.com/api/album/"+url[i]+"/detail"
     get_song(albumurl) #=> #download() => add_lyrics_to_flac()
