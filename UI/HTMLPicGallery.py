from pymongo import MongoClient
import uuid
import webbrowser
import os
from threading import Timer

def display_images(pic_info, title=''):
    html = _build_html(pic_info,title)
    filename = uuid.uuid4().hex+".html"
    text_file = open(filename, "w")
    text_file.write(html)
    text_file.close()
    webbrowser.get().open('file://' + os.path.realpath(filename))
    t = Timer(15.0, _remove_file, args=[filename])
    t.start()

def _remove_file(filename):
    os.remove(filename)

def _build_html(pic_info, title):

    top = '''<!DOCTYPE html>
<html>
<head>
<title>'''+title+'''</title>
<style>
div.gallery {
    margin: 5px;
    border: 1px solid #ccc;
    float: left;
    width: 180px;
}

div.gallery:hover {
    border: 1px solid #777;
}

div.gallery img {
    width: 180px;
    height: 180px;
}

div.desc {
    padding: 15px;
    text-align: center;
}
</style>
</head>
<body>'''
    mid = ''
    client = MongoClient('localhost', 27017)
    db = client['mwdb']
    table = db['LIU_commonterms']
    for index, d in enumerate(pic_info):
        t = table.find_one({'image': d['id']})
        if t is not None:
            mid = mid + '<div class ="gallery"><a target = "_blank"><img src = "'+t['imagepath']+'" width = "600" height = "400" ></a><div class ="desc" >'+d['info']+'</div></div>'

    bottom = '</body></html>'

    return top + mid + bottom