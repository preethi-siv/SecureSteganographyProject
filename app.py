from flask import Flask, render_template, request, send_from_directory
import os
from steganography import hide_data, extract_data

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        message = request.form["message"]
        if file and message:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)
            output_path = os.path.join(app.config["UPLOAD_FOLDER"], "stego_" + file.filename)
            hide_data(filepath, message, output_path)
            return f"Image processed! Download: <a href='/download/{output_path}'>Click here</a>"
    return render_template("index.html")

@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
