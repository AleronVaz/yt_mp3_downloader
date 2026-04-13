from flask import Flask, request, render_template, send_file, after_this_request 
import yt_dlp
import os
import time

app = Flask(__name__, template_folder='.')

# Create a downloads folder if it doesn't exist
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    youtube_url = request.form.get('youtube_url')
    
    if not youtube_url:
        return "Error: No URL provided", 400

    print(f"--- SERVER LOG ---")
    print(f"URL Received: {youtube_url}")

    # Instructions for yt-dlp
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
        },
        'extractor_args': {
            'youtube': {
                # This tells yt-dlp to use the bgutil plugin we added to requirements
                'po_token': ['web+'], 
            }
        },
        'nocheckcertificate': True,
        # We save it into the downloads folder
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
    }
    
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            # 1. Download the file
            info = ydl.extract_info(youtube_url, download=True)
            # 2. Get the actual filename created (with .mp3 extension)
            temp_filename = ydl.prepare_filename(info)
            base, ext = os.path.splitext(temp_filename)
            final_filename = base + ".mp3"

            @after_this_request
            def remove_file(response):
                try:
                    # We wait until the request is finished, then delete the file
                    time.sleep(1)  # Just to ensure the file is not in use
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

            # Add the "Permission Header" so JS can read the filename
            # Without this, your JS might just name everything "download.mp3"
            response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
            
            return response

    except Exception as e:
        print(f"❌ Error: {e}")
        return f"Backend Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)