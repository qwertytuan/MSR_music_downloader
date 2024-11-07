import os
import webbrowser
import requests




def download(url):
    try:
        response = requests.get(url, stream=True,timeout=10)
        response.raise_for_status()
        data=response.json()['data']
        for item in data:
            cid = item["cid"]
            name = item["name"]
            cover_url = item["coverUrl"]
          # print(f"CID: {cid}")
          # print(f"Name: {name}")
          # print(f"Cover URL: {cover_url}")
            with open("./html/output.txt", "a",encoding='utf-8') as file:
                file.write(f"CID: {cid}\nName: {name}\nCover URL: {cover_url}\n\n")

    except requests.exceptions.RequestException as e:
        #stop the program when get status code 404
        if response.status_code == 404:
            print("finished", response.status_code)
            exit()
        print("Error: ", e)
        
#main
url="https://monster-siren.hypergryph.com/api/albums"
if os.path.exists("./html/output.txt"): 
    os.remove("./html/output.txt")
download(url)
file =os.path.abspath("html/getalbum.html")
webbrowser.open(file,new=2)
