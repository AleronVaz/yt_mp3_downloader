from flask import Flask, request, render_template, send_file, after_this_request 
from pytubefix import YouTube
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

    try:
        # use_po_token=True is the main bypass for Render/Cloud servers
        yt = YouTube(youtube_url, use_po_token=True)
        
        # Select audio only
        audio_stream = yt.streams.get_audio_only()
        
        # Download file
        downloaded_file = audio_stream.download(output_path=DOWNLOAD_FOLDER)
        
        # Rename to .mp3
        base, ext = os.path.splitext(downloaded_file)
        final_filename = base + ".mp3"
        os.rename(downloaded_file, final_filename)

        @after_this_request
        def remove_file(response):
            try:
                time.sleep(1)
                if os.path.exists(final_filename):
                    os.remove(final_filename)
                    print(f"🗑️ Deleted: {final_filename}")
            except Exception as e:
                print(f"Cleanup error: {e}")
            return response

        return send_file(
            final_filename, 
            as_attachment=True, 
            download_name=os.path.basename(final_filename)
        )

    except Exception as e:
        print(f"❌ Pytube Error: {e}")
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)