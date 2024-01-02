#####################################################################################
# System : 사용 패키지
#####################################################################################
from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests 
from pymongo import MongoClient
from bson.json_util import dumps
from bson import ObjectId

#####################################################################################
# System : 기본 설정
#####################################################################################

# Flask 파일 세팅
app = Flask(__name__)

#####################################################################################
# System : 데이터베이스 세팅
#####################################################################################

# sw-jungle 테스트용 mongo cloud
client = MongoClient('mongodb+srv://yshwang:yshwang@cluster0.pi8yxg5.mongodb.net/?retryWrites=true&w=majority')
db_jungle = client.db_jungle

#####################################################################################
# Test : 정글 사전 입학시험(2024-01)
#####################################################################################
# 테스트 참여용 템플릿
@app.route('/jungle/test')
def render_jungle_test():
    return render_template('jungle/test.html')

# 완성본 
@app.route('/jungle/answer')
def render_jungle_answer():
    return render_template('jungle/answer.html')

@app.route('/api/jungle/todo', methods=["POST"])
def insert_jungle_todo():
    todo_receive = request.form['todo']
    db_jungle.todo.insert_one({"todo" : todo_receive, "done" : False})
    return jsonify({"msg" : "등록 완료!"})

@app.route('/api/jungle/todo')
def read_jungle_todo():
    all_todo = list(db_jungle.todo.find({}))
    for todo in all_todo:
        todo['_id'] = str(todo['_id'])
    return jsonify({"all_todo": all_todo})

@app.route('/api/jungle/todo/complete', methods=["POST"])
def complete_jungle_todo():
    id_receive = request.form['_id']
    db_jungle.todo.update_one({"_id" : ObjectId(id_receive)}, {"$set":{"done": True}})
    return jsonify({"msg" : "할 일 체크 완료!"})

@app.route('/api/jungle/todo/update', methods=["POST"])
def update_jungle_todo():
    id_receive = request.form['_id']
    todo_receive = request.form['todo']
    db_jungle.todo.update_one({"_id" : ObjectId(id_receive)}, {"$set":{"todo": todo_receive}})
    return jsonify({"msg" : "할 일 업데이트 완료!"})

@app.route('/api/jungle/todo/delete', methods=["POST"])
def delete_jungle_todo():
    id_receive = request.form['_id']
    db_jungle.todo.delete_one({"_id" : ObjectId(id_receive)})
    return jsonify({"msg" : "할 일 삭제 완료!"})


#####################################################################################
# System : Flask 웹 실행
#####################################################################################
if __name__ == "__main__":
    init_db()  
    app.run(debug=True)
