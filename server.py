from main import *
from flask import Flask, send_file, Response, request, jsonify, render_template
import os

app = Flask(__name__)

def file_name(list_item):
    try:
        data = []
        for file in list_item:
            file = file[:-4]
            data.append(file)
        return data
    except:
        return list_item[:-4]
        
def get_dir(dirname):
    listdir = os.listdir(f'./chats/{dirname}/')
    listdir = file_name(listdir)
    return listdir

def get_dir_item(dirname,name):
    with open(f'./chats/{dirname}/{name}.txt', 'r') as f:
        content = f.read()
        return content

def add_dir_item(dirname, name, content):
    with open(f'./chats/{dirname}/{name}.txt', 'x') as f:
        f.write(content)

def edit_dir_item(dirname, name, content):
    with open(f'./chats/{dirname}/{name}.txt', 'w') as f:
        f.write(content)

def delete_dir_item(dirname, name):
    myfile = f'./chats/{dirname}/{name}.txt'
    if os.path.isfile(myfile):
        os.remove(myfile)
        return True
    raise Exception('not a file')
    
@app.route('/', methods=['GET', 'POST'])
def welcome():
    return jsonify({'body':'Root of GPT-3 Python', 'status':200})

@app.route('/get/<dirname>', methods=['GET'])
def route_get_dir(dirname):
    try:
        listdir = get_dir(dirname)
        return jsonify({
            'body':{
                'data':listdir,
                'name':dirname,
                },
            'status':200,
            })
    except:
        return jsonify({
            'status':304,
            })

@app.route('/get/<dirname>/<name>', methods=['GET'])
def route_get_dir_item(dirname,name):
    try:
        item = get_dir_item(dirname,name)
        return jsonify({
            'body':item,
            'status':200,
            })
    except:
        return jsonify({
            'status':304,
            })

@app.route('/add/<dirname>/<name>/<content>', methods=['GET', 'POST'])
def route_add_dir_item(dirname, name, content):
    try:
        add_dir_item(dirname, name, content)
        return jsonify({
            'status':200,
            })
    except:
        return jsonify({
            'status':304,
            })

@app.route('/edit/<dirname>/<name>/<content>', methods=['GET', 'PUT'])
def route_edit_dir_item(dirname, name, content):
    try:
        edit_dir_item(dirname, name, content)
        return jsonify({
            'status':200,
            })
    except:
        return jsonify({
            'status':304,
            })

@app.route('/delete/<dirname>/<name>', methods=['GET', 'DELETE'])
def route_delete_dir_item(dirname, name):
    try:
        delete_dir_item(dirname, name)
        return jsonify({
            'status':200,
            })
    except:
        return jsonify({
            'status':304,
            })

@app.route('/chat', methods=['GET'])
def route_chat():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2023, debug=True)