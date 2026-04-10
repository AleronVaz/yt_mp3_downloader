import yt_dlp

def download_audio(url):
    # The 'instructions' for the library
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(playlist_title)s/%(title)s.%(ext)s',
    }

    print(f"--- Accessing URL: {url} ---")
    
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        print("\n✅ Success! Your MP3 is ready.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    link = input("Paste the YouTube link here: ")
    download_audio(link)