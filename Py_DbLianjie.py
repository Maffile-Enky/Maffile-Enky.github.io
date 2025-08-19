from flask_sqlalchemy import SQLAlchemy
import pymysql 
from flask import Flask,render_template,request,redirect,url_for,session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:060322@localhost:3306/data_new_1"
db = SQLAlchemy()
db.init_app(app)


class Dept(db.Model):

    __tablename__ = 'dept'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    indept = db.Column(db.String(20))
    password = db.Column(db.String(20))

@app.route('/dept_info',methods=['GET'])
def dept_info():
    num = request.args.get('Num')
    num = Dept.query.filter_by(id=num).first()
    return render_template('name_search.html',num=num)

@app.route('/dept_all',methods=['GET'])
def dept_all():
    depts = Dept.query.all()
    return render_template('dept_all.html',depts=depts)

@app.route('/dept_add', methods=["GET", "POST"])
def dept_add():
    if request.method == 'POST':
        name = request.form['name']
        new_dept = Dept(name=name)
        db.session.add(new_dept)
        db.session.commit()
        return redirect(url_for('dept_all'))
    else:
        return render_template('dept_add.html')

@app.route('/dept_del', methods=['POST','GET'])
def dept_del():
    num = request.form.get('Num')
    if not num:
        return render_template('dept_del.html')
    dept = Dept.query.filter_by(id=num).first()
    if dept:
        db.session.delete(dept)
        db.session.commit()
    return redirect(url_for('dept_all'))

@app.route('/dept_power', methods=['GET', 'POST'])
def dept_power():
    depts = Dept.query.all()  # 查询所有部门
    selected_dept = None
    powers = []
    if request.method == 'POST':
        dept_id = request.form.get('dept_id')
        selected_dept = Dept.query.filter_by(id=dept_id).first()
        # powers = ...  # 根据部门查询权限
    return render_template('dept_power.html', depts=depts, selected_dept=selected_dept, powers=powers)

@app.route('/dept_more',methods=['GET'])
def dept_more():
    return render_template('dept_more.html')


@app.route('/dept_login', methods=['GET','POST'])
def dept_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        dept = Dept.query.filter_by(name=username).first()

        if not dept or dept.password != password:
            return render_template('dept_login.html', error='用户名不存在或密码错误')

        # 登录成功
        
        return redirect(url_for('index'))  # 跳转到主页

    return render_template('dept_login.html')


@app.route('/',)
@app.route('/index')
def index():
    return render_template('index.html')    

if __name__ == '__main__':
    app.run(debug=True)
