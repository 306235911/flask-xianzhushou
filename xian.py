# -*- coding:utf-8 -*-
import os
# falsk 模板渲染 会话 重定向 从修饰器生成url
from flask import Flask, render_template, session, redirect, url_for
# 命令行工具
from flask.ext.script import Manager, Shell
# 模板
from flask.ext.bootstrap import Bootstrap
# 时间
from flask.ext.moment import Moment
# 表单
from flask.ext.wtf import Form
# 字符串表单 提交按钮
from wtforms import StringField, SubmitField
# 验证提交的表单是否为空
from wtforms.validators import Required
# 数据库
from flask.ext.sqlalchemy import SQLAlchemy
# 数据库迁移
from flask.ext.migrate import Migrate, MigrateCommand
from flask import request

# 得到当前绝对地址
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# 密钥
app.config['SECRET_KEY'] = 'hard to guess string'
# 数据库地址
app.config['SQLALCHEMY_DATABASE_URI'] =('mysql://root:306235911@localhost/xian')
# 每次结束会话前提交
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# 初始化命令行 模板 时间 数据库 数据库迁移模块 邮箱模块
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db' , MigrateCommand)
# 
# 
# 
# 数据库模型role
class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    detal = db.Column(db.String(140))
    # 以后可尝试使用外键
    img1 = db.Column(db.String(70))
    img2 = db.Column(db.String(70))
    img3 = db.Column(db.String(70))
    title = db.Column(db.String(20))

    def __repr__(self):
        return '<Item %r>' % self.name

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(64) , unique=True)
    users = db.relationship('User' , backref='role')
    
    def __rerp__(self):
        return '<Role %r>' % self.name
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(64) ,unique=True , index = True)
    role_id = db.Column(db.Integer , db.ForeignKey('roles.id'))
    
    def __repr__(self):
        return '<User %r>' % self.username


# # 输入姓名的表单
# class itemForm(Form):
#     itemName = StringField(validators=[Required()])
#     submit = SubmitField('搜索')
# 

# 404错误处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 500错误处理
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# 主页面
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form.get('search','')
        item = Item.query.filter_by(name = data).all()
        if item:
            return render_template('myindex.html' , items = item)
        else:
            return render_template('haveNot.html')
    items = Item.query.all()
    return render_template('myindex.html', items = items )
    # return render_template('oneitem.html')

@app.route('/item/<itemName>')
def item(itemName):
    item = Item.query.filter_by(name = itemName).first()
    return render_template('item.html' , itemName = item)

@app.route('/title/<titleName>')
def title(titleName):
    title = Item.query.filter_by(title = titleName).all()
    return render_template('myindex.html' , items = title)

if __name__ == '__main__':
    manager.run()
