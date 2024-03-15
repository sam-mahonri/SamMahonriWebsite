from .... import app
import os

def delete_fileurl(url):
    try:
        filename = url.split('/image/')[1]
        path = app.config["UPLOAD_PATH"]
        os.remove(path + "/" + filename)
        return True
    except Exception as e:
        print("\n\nErro" + str(e) + "\n\n")
        return False