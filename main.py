from pytubefix import YouTube
import os

@app.route('/convert', methods=['POST'])
def convert():
    youtube_url = request.form.get('youtube_url')
    if not youtube_url:
        return "Error: No URL provided", 400

    try:
        # use_oauth=False keeps it simple for now
        # use_po_token=True is the magic bypass
        yt = YouTube(youtube_url, use_po_token=True)
        
        # Select the best audio stream
        audio_stream = yt.streams.get_audio_only()
        
        # Download (it saves as .m4a or .webm usually)
        downloaded_file = audio_stream.download(output_path=DOWNLOAD_FOLDER)
        
        # Force rename to .mp3 so your frontend stays happy
        base, ext = os.path.splitext(downloaded_file)
        final_filename = base + ".mp3"
        os.rename(downloaded_file, final_filename)

        @after_this_request
        def remove_file(response):
            try:
                time.sleep(1)
                if os.path.exists(final_filename):
                    os.remove(final_filename)
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