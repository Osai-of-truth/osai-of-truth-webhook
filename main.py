
from flask import Flask, request, jsonify
from moviepy.editor import *
import dropbox
import uuid
import os

app = Flask(__name__)

# Dropbox token
DROPBOX_TOKEN = (
    "sl.u.AFpndYcaNt6Fewd5VKPFoTF3IvJA6-Btz9PNabSYPC1AeD1M6uZE6xvlpGvw0ExDgYcAU9kTz0wBix"
    "TGY7lQvbMBTrvXCfshzUIBCkQ_0y5DLcRhFWumXAB2H6L5fqj8CSHrEO651LH637js0emAbEVAfC6TzJsNbH"
    "H6LsP_Ox4lhI20Nx2ej-c0S0OsVUqbWHm-7Dm0NPpBHP6xZSIjbKpOxmed1Je6oeoN5tMDk-0NAaP3lBHzB_"
    "UcyC3C6fIvT3dmbal_ROoWQw0nT4CuEESRBF78xUIYIKRqd12bw2KX1wQHLX4ViMt3EABxJYTGRehgZfMMPc"
    "zpGibrrY-sIrrEtG3UGqVdPML4dAYRaMgWfKlDNe0EsmUDK7x1rER6kpTIA4gihpltzstCprYe8fOMsSRkpb"
    "EmPOOaASh7g7IrfJ3d8e2UejvwQf8RZTIUkonVEOj3r2nEQQuBHWC87dW1mmmZlE6p6ZJsSAwqxYb2Bi-a3ig"
)

@app.route('/generate', methods=['POST'])
def generate_video():
    data = request.get_json()
    prompt = data.get("prompt", "வாழ்க்கை ஒரு பாடம்.")
    filename = f"{uuid.uuid4()}.mp4"

    # Create video
    duration = 7
    bg_color = (10, 10, 10)
    text_color = 'white'
    font_size = 70

    txt_clip = TextClip(prompt, fontsize=font_size, color=text_color, method='caption')
    txt_clip = txt_clip.set_duration(duration).set_position('center')
    bg_clip = ColorClip(size=(1080, 1920), color=bg_color, duration=duration)
    final_clip = CompositeVideoClip([bg_clip, txt_clip])
    final_clip.write_videofile(filename, fps=24)

    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    dropbox_path = f"/osai_of_truth/{filename}"
    with open(filename, "rb") as f:
        dbx.files_upload(f.read(), dropbox_path, mute=True, mode=dropbox.files.WriteMode.overwrite)

    shared_link = dbx.sharing_create_shared_link_with_settings(dropbox_path)
    video_url = shared_link.url.replace("?dl=0", "?raw=1")
    os.remove(filename)

    return jsonify({"video_url": video_url})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
