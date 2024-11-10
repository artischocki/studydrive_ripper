from flask import Flask, render_template_string, request, redirect, url_for
import webbrowser
import requests
import re
 
index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document Downloader</title>
</head>
<body>
    <form action="/download" method="post">
        <label for="url">URL:</label>
        <input type="text" id="url" name="url" style="width: 450px;" required>
        <button type="submit">Download</button>
    </form>
</body>
</html>
"""
 
not_found_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document Not Found</title>
</head>
<body>
    <h1>Document Not Found</h1>
    <p>The provided URL is not valid or the document could not be found.</p>
    <a href="/">Go back</a>
</body>
</html>
"""
 
app = Flask(__name__)
 
def download(url):
    if not url.startswith("https://www.studydrive.net/"):
        return "/not_found: Url doesn't start with https://www.studydrive.net/"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Unable to fetch URL ({response.status_code})")
        return "/not_found"
    body = response.text
    regex_pattern = r'token=(.*?)"'
    match = re.search(regex_pattern, body)
    if not match:
        print("no match! document id")
        return "/not_found: Couldn't get Document-Id"
    token = match.group(1)
    doc_id = url.split("/")[-1].split("?")[0]
    print(f"doc_id={doc_id}")
    filename_pattern = r'"filename":"(.*?)"'
    filename_match = re.search(filename_pattern, body)
    if not filename_match:
        print("no match! filename")
        return "/not_found: Couldn't get file_type"
    file_name = filename_match.group(1)
    if "pdf" in file_name:
        redirect_url = f"https://cdn.studydrive.net/d/prod/documents/{doc_id}/original/{doc_id}.pdf?token={token}"
    elif "docx" in file_name:
        redirect_url = f"https://cdn.studydrive.net/d/prod/documents/{doc_id}/original/{doc_id}.docx?token={token}"
    elif "jpeg" in file_name:
        redirect_url = f"https://cdn.studydrive.net/d/prod/documents/{doc_id}/original/{doc_id}.jpeg?token={token}"
    elif "png" in file_name:
        redirect_url = f"https://cdn.studydrive.net/d/prod/documents/{doc_id}/original/{doc_id}.png?token={token}"
    elif "jpg" in file_name:
        redirect_url = f"https://cdn.studydrive.net/d/prod/documents/{doc_id}/original/{doc_id}.jpg?token={token}"
    else:
        print("filename, doesnt match pdf,docx,jpeg,png,jpg", "currentfile_name:", file_name)
        return "/not_found: file_type doesnt match: pdf,docx,jpeg,png,jpg\n Current Filename: " + file_name + " to fix this please add the file type!"
    return redirect_url
 
@app.route('/')
def index():
    return render_template_string(index_html)
 
@app.route('/download', methods=['POST'])
def handle_download():
    url = request.form['url']
    redirect_url = download(url)
    if "/not_found" in redirect_url:
        error_message = redirect_url.replace("/not_found", "ERROR")
        print(error_message)
        return render_template_string(not_found_html)
    else:
        webbrowser.open_new_tab(redirect_url)
        return redirect(url_for('index'))
 
if __name__ == '__main__':
    webbrowser.open_new_tab('http://127.0.0.1:45321/')
    app.run(port=45321)
 

