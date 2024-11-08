import requests
import subprocess

def download_and_convert_ts(url, output_file_prefix, temp_file,file_name,choice):

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(temp_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    except requests.exceptions.RequestException as e:
        #stop the program when get status code 404
        if response.status_code == 404:
            print("finished", response.status_code)
            file_name1 ="copy /b temp**.ts "+file_name + ".ts"
            subprocess.call(file_name1, shell=True)
            if choice == "y":
                subprocess.call("del temp**.ts", shell=True)
                exit()
            exit()
        print("Error downloading TS file:", e)
            
#main
url=input("Enter the url of the video: ")
file_name=input("Enter the name of the video: ")
choice=input("Do you want to delete the temp files? (y/n): ")
if choice == "y":
    choice = "y"
elif choice == "n":
    choice = "n"
else:
    print("Invalid choice")
    exit()
url= url[:-8]
output_file_prefix = "video"
for i in range(1,1000): 
    j='{:05d}'.format(i)
    url2=url+str(j)+".ts"
    temp_file = "temp"+str('{:02d}'.format(i))+".ts"
    download_and_convert_ts(url2, output_file_prefix,temp_file,file_name,choice)
