from datetime import datetime
from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.vmgfjkn.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/show_diary', methods=['GET'])
def showdiary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})
    #sample_receive = request.args.get('sample_give')
    #print(sample_receive)
    #return jsonify({'message': 'data diterima.'})

@app.route('/diary', methods=['POST'])
def savediary():
    #sample_receive = request.form['sample_give']
    #print(sample_receive)
    file = request.files["file_give"]
    #untuk cek ekstensi file (jpg atau png dll)
    ext = file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime("%Y-%m-%d %H-%M-%S")

    img_name = f'static/post-{mytime}.{ext}'
    file.save(img_name)  

    pfp = request.files["pfp_give"]
    extpfp = pfp.filename.split('.')[-1]
    pfp_name = f'static/pfp-{mytime}.{extpfp}'
    pfp.save(pfp_name)  

    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    todaydate = today.strftime("%Y-%m-%d")

    doc = {
        'file': img_name,
        'pfp': pfp_name,
        'title': title_receive,
        'content': content_receive,
        'date': todaydate
    }

    db.diary.insert_one(doc)
    return jsonify({'msg': 'POST complete'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
