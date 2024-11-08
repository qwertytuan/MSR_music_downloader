import os
import requests
from tqdm import tqdm
from mutagen.wave import WAVE
from mutagen.id3 import USLT,TPE1, Encoding


def getcid(url):
    try:
        response = requests.get(url, stream=True,timeout=100)
        response.raise_for_status()
        data=response.json()['data']
        for item in data:
            cid = item["cid"]

            albumurl = "https://monster-siren.hypergryph.com/api/album/"+cid+"/detail"
            get_song(albumurl)
    except requests.exceptions.RequestException as e:
        #stop the program when get status code 404
        if response.status_code == 404:
            print("finished", response.status_code)
            exit()
        print("Error: ", e)

def get_song(albumurl):
    try:
        response = requests.get(albumurl,stream=True,timeout=100)
        response.raise_for_status()
        data=response.json()
        songs = data['data']['songs']
        albumname = data['data']['name']
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
            download(url,albumname)
    except requests.exceptions.HTTPError as err:
        print("Error: ", err)
        exit()

def download(url,albumname):
    try:
        response = requests.get(url, stream=True,timeout=100)
        response.raise_for_status()
        data=response.json()
        file_name= data['data']['name']
        songurl= data['data']['sourceUrl']
        artists = data['data']['artists']
        temp="temp.wav"
        checkmp3 = songurl.split('.')[-1][-3:]
        if checkmp3 == "mp3":
         file_name_wav_mp3=file_name+".mp3"
        elif checkmp3 == "wav":
         file_name_wav_mp3=file_name+".wav"
        #get song url
        dwnsong= requests.get(songurl, stream=True,timeout=100)
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
        print("Song downloaded")
        #get lyrics url
        lrcurl = data['data']['lyricUrl']
        if lrcurl == None:
            print("No lyrics found")
            return
        else:
            print("Lyrics found")
            dwnlrc= requests.get(lrcurl, stream=True)
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
            if checkmp3 == "wav":
                add_lyrics_to_wav(file_name_wav_mp3,lrc,artists,albumname)
            else:
                return
    except requests.exceptions.RequestException as e:
        print("Error: ", e)
        #stop the program when get status code 404
        if response.status_code == 404:
         print("finished", response.status_code)
         exit()

#function to add lyrics to the song that is in wav format
def add_lyrics_to_wav(file_name_wav_mp3, lrc,artists,albumname):
    # Load the WAV file
    audio = WAVE(os.path.join(albumname,file_name_wav_mp3))

    # Create an ID3 tag if it doesn't exist
    if not audio.tags:
        audio.add_tags()

    # Add lyrics to the ID3 tag
    with open(os.path.join(albumname+"/lyrcs",lrc), 'r', encoding='utf-8') as lrc:
        lrc = lrc.read()
    audio.tags.add(
        USLT(
            encoding=Encoding.UTF8,
            lang='eng',
            desc='Lyrics',
            text=lrc
        )
    )
    audio.tags.add(
        TPE1(
            encoding=Encoding.UTF8,
            text=artists
        )
    )
    # Save the changes
    audio.save()
    print("Lyrics added to the song")

#main
url="https://monster-siren.hypergryph.com/api/albums"
getcid(url)
