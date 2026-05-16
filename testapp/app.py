from flask import Flask, render_template, request, send_file
import os
from pydub import AudioSegment

app = Flask(__name__)

# 保存フォルダ
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# フォルダパスだけでなく、最後に「\ffmpeg.exe」まで書くのがコツです
#ffmpeg_path = r"C:\Users\obata\Documents\pyhon514\ffmpeg-8.1.1-essentials_build\ffmpeg-8.1.1-essentials_build\bin\ffmpeg.exe"
#ffprobe_path = r"C:\Users\obata\Documents\pyhon514\ffmpeg-8.1.1-essentials_build\ffmpeg-8.1.1-essentials_build\bin\ffprobe.exe"

#AudioSegment.converter = ffmpeg_path
#AudioSegment.ffprobe = ffprobe_path
# --------------------

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        return render_template('index.html')

    if 'file' not in request.files:
        return "ファイルがありません", 400

    file = request.files['file']

    if file.filename == '':
        return "ファイル名が空です", 400

    input_filename = file.filename

    output_filename = (
        input_filename.rsplit('.', 1)[0]
        + ".mp3"
    )

    input_path = os.path.join(
        UPLOAD_FOLDER,
        input_filename
    )

    output_path = os.path.join(
        UPLOAD_FOLDER,
        output_filename
    )

    try:

        # M4A保存
        file.save(input_path)

        print(f"保存完了: {input_path}")

        # MP3変換
        audio = AudioSegment.from_file(
            input_path,
            format="m4a"
        )

        audio.export(
            output_path,
            format="mp3"
        )

        print(f"変換完了: {output_path}")

        # 存在確認
        if not os.path.exists(output_path):
            return (
                f"変換後ファイルがありません: {output_path}",
                500
            )

        # ダウンロード送信
        return send_file(
            output_path,
            as_attachment=True
        )

    except Exception as e:

        print(f"システムエラー: {str(e)}")

        return (
            f"エラー発生: {str(e)}",
            500
        )

if __name__ == '__main__':
    app.run(debug=True, port=5001)