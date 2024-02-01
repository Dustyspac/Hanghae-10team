from flask import Flask, render_template, request
import requests,os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

class Member(db.Model):
    member_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    pwd = db.Column(db.String, nullable=False)
    memos = relationship('Memo', backref='member', lazy=True)
    todo_lists = relationship('ToDoList', backref='member', lazy=True)
    address_books = relationship('AddressBook', backref='member', lazy=True)
    diaries = relationship('Diary', backref='member', lazy=True)

class Memo(db.Model):
    memo_id = db.Column(db.Integer, primary_key=True)
    main_text = db.Column(db.Text, nullable=False)
    edit_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    member_id = db.Column(db.String, db.ForeignKey('member.member_id'), nullable=False)

class ToDoList(db.Model):
    todolist_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    deadline = db.Column(db.Date, nullable=True)
    is_complete = db.Column(db.Boolean, nullable=False, default=False)
    member_id = db.Column(db.String, db.ForeignKey('member.member_id'), nullable=False)

class AddressBook(db.Model):
    address_id = db.Column(db.Integer, primary_key=True)
    member_name = db.Column(db.String, nullable=False)
    role_mbti = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String, nullable=False)
    project = db.Column(db.String, nullable=False)
    member_id = db.Column(db.String, db.ForeignKey('member.member_id'), nullable=False)

class Diary(db.Model):
    diary_id = db.Column(db.Integer, primary_key=True)
    main_text = db.Column(db.Text, nullable=False)
    edit_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    member_id = db.Column(db.String, db.ForeignKey('member.member_id'), nullable=False)

@app.route("/memo/")
def memo():

    # 예시 메모
    memo_list = []
    for i in range(100):
        memo = {
            'text': i+1,
            'date': i+2000
        }
        memo_list.append(memo)

    memo_per_page= 6
    # 클라이언트의 현재 페이지 숫자(없으면 기본적으로 1페이지)
    page = request.args.get('page',1,type=int)

    # 내보내야 할 데이터 정보의 start index와 end index
    start_index = (page-1)*memo_per_page
    end_index = start_index+memo_per_page

    # 내보낼 메모들 리스트로 저장
    current_page_memo = memo_list[start_index:end_index]

    total_memos = len(memo_list)
    total_pages = (total_memos+memo_per_page-1)//memo_per_page
    
    return render_template('memo.html', data=current_page_memo, page_num=total_pages)


    # 예시 Adress

# 추가한 데이터를 화면에 표시
@app.route("/AddressBook/")
def member():
        member_list = AddressBook.query.all()
        return render_template('address.html', data=member_list)


@app.route("/AddressBook/Add/",methods=["GET"])
def add_member():
    # form 에서 보낸 데이터 받아오기
        member_name_receive = request.args.get("member_name")
        role_mbti_receive = request.args.get("role_mbti")
        image_url_receive = request.args.get("image_url")
        address_id_receive = request.args.get("address_id")
        project_receive = request.args.get("project")
        member_id_receive = request.args.get("member_id")


    # 데이터를 DB에 저장
        adress = AddressBook (member_name=member_name_receive, role_mbti=role_mbti_receive, image_url=image_url_receive, address_id=address_id_receive, project=project_receive, member_id=member_id_receive)
        db.session.add(adress)
        db.session.commit()
        print(project_receive)
        return render_template('address.html')

if __name__ == '__main__':
    app.run()