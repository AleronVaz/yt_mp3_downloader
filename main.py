from flask import Flask, request, render_template, send_file, after_this_request 
import yt_dlp
import os
import time
import sys
import webbrowser
from threading import Timer
from threading import Thread
import signal

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

app = Flask(__name__, 
            template_folder=resource_path('.'), 
            static_folder=resource_path('static'))

# Create a downloads folder if it doesn't exist
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

# Global variable to track last heartbeat time
last_seen = time.time()

@app.route('/heartbeat')
def heartbeat():
    global last_seen
    last_seen = time.time()
    return "OK", 200

def watchdog():
    global last_seen
    while True:
        time.sleep(10)  # Check every 10 seconds
        if time.time() - last_seen > 30:  # If no heartbeat for 30 seconds
            print("⚠️ No heartbeat detected. Shutting down server.")
            os.kill(os.getpid(), signal.SIGTERM)  # Shutdown the server

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    youtube_url = request.form.get('youtube_url')
    format_type = request.form.get('format_type')
    quality = request.form.get('quality')
    
    if not youtube_url:
        return "Error: No URL provided", 400

    print(f"--- SERVER LOG ---")
    print(f"URL: {youtube_url} | Format: {format_type} | Quality: {quality}")

    # Instructions for yt-dlp
    options = {
        'ffmpeg_location': resource_path('.'),
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
        },
        'extractor_args': {
            'youtube': {
                'po_token': ['web+'], 
            }
        },
        'nocheckcertificate': True,
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
    }

    # DYNAMIC FORMAT LOGIC
    if format_type == 'mp3':
        options.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192' if quality == 'high' else '128',
            }],
        })
    else:  # MP4 Logic
        if quality == 'high':
            options.update({
                'format': 'bestvideo[vcodec^=avc1]+bestaudio[acodec^=mp4a]/best[ext=mp4]/best',
                'merge_output_format': 'mp4', # Forces the final file to be MP4
            })
        else:
            options['format'] = 'worstvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
    
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            # 1. Download the file
            info = ydl.extract_info(youtube_url, download=True)
            temp_filename = ydl.prepare_filename(info)
            
            # 2. Get the correct final filename
            if format_type == 'mp3':
                base, ext = os.path.splitext(temp_filename)
                final_filename = base + ".mp3"
            else:
                final_filename = temp_filename.rsplit('.', 1)[0] + '.mp4'

            @after_this_request
            def remove_file(response):
                try:
                    time.sleep(1)
                    if os.path.exists(final_filename):
                        os.remove(final_filename)
                        print(f"🗑️ Successfully deleted: {final_filename}")
                except Exception as error:
                    print(f"⚠️ Error deleting file: {error}")
                return response

            print(f"✅ Success! Prepared: {final_filename}")
            
            # 3. Send the file back to the browser
            response = send_file(
                final_filename, 
                as_attachment=True, 
                download_name=os.path.basename(final_filename)
            )

            response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
            return response

    except Exception as e:
        print(f"❌ Error: {e}")
        return f"Backend Error: {str(e)}", 500

if __name__ == '__main__':
    Timer(1.5, open_browser).start()
    Thread(target=watchdog, daemon=True).start()
    app.run(host='127.0.0.1', port=5000)