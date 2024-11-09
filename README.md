# English
# Attention!! 
For windows users that experience `Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work warn("Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work", RuntimeWarning")`

PLEASE Download [ffmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z) extract and add bin file to system and user PATH in setting "Edit the system environment variables"
### OR
USING SCRIPT FROM FOLDER NONFLAC
## Step 1: Install Python 3 or later
Run the command `pip install ffmpeg requests mutagen tqdm pydub` or `python3 pip install ffmpeg requests mutagen tqdm pydub in your terminal`. This will install the necessary Python libraries for this task.
## Step 2: Run the getalbum.py script
Execute the command python3 <filename> (replace <filename> with the actual name of the script) to save the existing MSR albums into a file named output.txt located in the "html" folder. You'll be prompted to select this file.
## Step 3: Open getalbum.html in Chrome (optional)
If the file doesn't open automatically in your browser, manually open getalbum.html in Google Chrome and select the output.txt file from the "html" folder.
## Step 4: Find the CID of the album you want to download
Locate the specific CID for the album you're interested in downloading.
## Step 5: Run downloadmusic.py and input CIDs
Execute the downloadmusic.py script and input the CIDs of the albums you want to download.

# Vietnamese
# CHÚ Ý!!
Ai dùng windows bị tình trạng  `Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work warn("Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work", RuntimeWarning")`

Hãy tải [ffmpeg](https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z), giải nén, và thêm file bin vào PATH của system và user trong cài đặt "Edit the system environment variables"
### HOẶC 
DÙNG SCRIPT TRONG TỆP NONFLAC
## Step 1: Cài python 3. trở lên 
Chạy lệnh `pip install ffmpeg requests mutagen tqdm pydub` hoặc `python3 pip install ffmpeg requests mutagen tqdm pydub`.
## Step 2: Chạy file getalbum.py bằng lệnh python3 <tên file> để lưu các albums hiện có của MSR vào file output.txt trong folder html, nhấn vào chọn file và di chuyển chọn output.txt trong folder html
( bỏ qua Step 3 nếu file đã tự mở trên trình duyệt)
## Step 3: Chạy file getalbum.html bằng chrome và chọn file output.txt trong folder html,
## Step 4: Tìm số CID của album mà bạn muốn tải.
## Step 5: Chạy file downloadmusic.py rồi điền các CIDs của album vào.


