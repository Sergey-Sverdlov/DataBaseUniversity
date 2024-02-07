from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2
from sqlalchemy import create_engine
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
# engine = create_engine('postgresql://localhost/postgres')
global cursor

app = Flask(__name__)
app.secret_key = 'some secret salt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://unregistered:1@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

manager = LoginManager(app)
try:
    connection = psycopg2.connect(user="unregistered",
                                  password="1",
                                  host="localhost",
                                  port="5432",
                                  database="postgres")
    cursor = connection.cursor()
except:
    print("Подключение к БД не выполнено")

class Name_speciality(db.Model, UserMixin):
    id_speciality = db.Column(db.INTEGER, primary_key=True)
    id_university = db.Column(db.INTEGER)
    number_speciality = db.Column(db.String(1000))
    name_speciality = db.Column(db.String(1000))

    def __repr__(self):
        return '<Admin %r' % self.id_speciality

class Rank_speciality(db.Model, UserMixin):
    id_speciality = db.Column(db.INTEGER, primary_key=True)
    rank_speciality = db.Column(db.INTEGER)

class Query (db.Model, UserMixin):
    id = db.Column(db.INTEGER, primary_key=True)
    intro = db.Column(db.String(1000))
    full_text = db.Column(db.String(5000))
    def __repr__(self):
        return '<Admin %r' % self.id

class Users (db.Model, UserMixin):
    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(500))
    email = db.Column(db.String(50), unique=True)
    mobile = db.Column(db.String(50), unique=True)
    university_selected = db.Column(db.String(70))
    type_user = db.Column(db.String(20))

    def __repr__(self):
        return '<User %r' % self.id

class University (db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(30))
    year_construction = db.Column(db.INTEGER)
    year_repair = db.Column(db.INTEGER)
    count_student = db.Column(db.INTEGER)
    min_cost = db.Column(db.INTEGER)
    intro = db.Column(db.String(80))
    about = db.Column(db.String(500))

    def __repr__(self):
        return '<University %r' % self.id

class MaleFemale(db.Model):
    id_university = db.Column(db.INTEGER, primary_key=True)
    count_male = db.Column(db.INTEGER)
    count_female = db.Column(db.INTEGER)
    def __repr__(self):
        return '<Male_Female %r' % self.id

class rank_university(db.Model):
    id_university = db.Column(db.INTEGER, primary_key=True)
    position_raex = db.Column(db.INTEGER)
    position_qs = db.Column(db.INTEGER)
    position_the = db.Column(db.INTEGER)

    def __repr__(self):
        return '<Rank_university %r' % self.id


@app.route('/home')
@app.route('/')
def index():
    try:
        return render_template("index.html", username=current_user.username, type_user = current_user.type_user)
    except:
        return render_template("index.html")



@app.route('/create_article', methods=['POST', 'GET'])
@login_required
def create_article():
    if (current_user.type_user == 'admin'):
        if request.method == "POST":
             name = request.form['name']
             year_construction = request.form['year_construction']
             year_repair = request.form['year_repair']
             count_student = request.form['count_student']
             min_cost = request.form['min_cost']
             intro = request.form['intro']
             about = request.form['about']
             male = request.form['male']
             female = request.form['female']
             qs = request.form['qs']
             the = request.form['the']
             raex = request.form['raex']
             print("here")
             cursor.execute('select id from university ORDER BY ID DESC LIMIT 1')

             new_id = cursor.fetchone()[0] + 1
             try:
                 university = University(id=new_id, name=name, year_construction=year_construction, year_repair=year_repair, count_student=count_student, min_cost=min_cost, intro=intro, about=about)
                 db.session.add(university)
                 male_female = MaleFemale(id_university=new_id, count_male=male, count_female=female)
                 db.session.add(male_female)

                 position = rank_university(id_university=new_id, position_raex=raex, position_qs=qs, position_the=the)
                 db.session.add(position)
             except:
                 return render_template("create_article.html")

             db.session.commit()
             return redirect('/')
        else:
            return render_template("create_article.html")
    else:
        return render_template("unauthorized.html")



@manager.user_loader
def load_user(user_id):
    global cursor
    if Users.query.get(user_id):
        user_name = Users.query.get(user_id).type_user
        if user_name == 'admin':
            app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:12345@localhost/postgres'
            connection = psycopg2.connect(user="admin",
                                          password="123453",
                                          host="localhost",
                                          port="5432",
                                          database="postgres")
            cursor = connection.cursor()
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://registered:123@localhost/postgres'
            connection = psycopg2.connect(user="registered",
                                          password="1233",
                                          host="localhost",
                                          port="5432",
                                          database="postgres")
            cursor = connection.cursor()
        return Users.query.get(user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('confirm')
        mobile = request.form.get('mobile')
        if password_confirm != password or not email or not name or not mobile:
            return render_template("signup.html")
        hash_password = generate_password_hash(password)
        try:
            new_user = Users(id=Users.query.order_by(Users.id).all().__len__()+1, username=username, password=hash_password, email=email, mobile=mobile, type_user = "user")
            db.session.add(new_user)
            db.session.commit()
        except:
            return redirect('/register')
        return redirect('/login')
    else:
        return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            if login and password:
                user = Users.query.filter_by(username=username).first()
                if user and check_password_hash(user.password, password):
                    login_user(user)
                return redirect('/')
        except:
            return render_template("Login.html")
    else:
        return render_template("Login.html")

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    global cursor
    logout_user()
    cursor.close()
    connection = psycopg2.connect(user="unregistered",
                                  password="12",
                                  host="localhost",
                                  port="5432",
                                  database="postgres")
    cursor = connection.cursor()
    return redirect('/')







@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():

    universities = db.session.query(University.id, University.name, University.intro).all()
    return render_template("posts.html", universities=universities, my_title = "Все университеты на сайте")

@app.route('/posts/<int:id>')
@login_required
def post_detail(id):
    university = University.query.get(id)
    male_female = MaleFemale.query.get(id)
    rank = rank_university.query.get(id)

    cursor.execute('select * from name_speciality join Rank_speciality on name_speciality.id_speciality = rank_speciality.id_speciality where name_speciality.id_university = {}'.format(id))
    records = cursor.fetchall()

    return render_template("post_detail.html", university=university, male_female=male_female, rank=rank, type_user = current_user.type_user, speciality = records)


@app.route('/university/<int:id>/add_to_selected')
def add_to_selected(id):
    cur_user = Users.query.get(current_user.id)
    if (cur_user.university_selected):
        cur_user.university_selected += str(id) + ';'
    else:
        cur_user.university_selected = str(id) + ';'
    db.session.commit()
    return redirect("/posts")



@app.route('/posts/<int:id>/delete')
def post_delete(id):
    if (current_user.type_user == "admin"):
        university = University.query.get_or_404(id)
        # try:
        male_female = MaleFemale.query.get_or_404(id)
        rank_univer = rank_university.query.get_or_404(id)
        db.session.delete(rank_univer)
        db.session.commit()
        db.session.delete(male_female)
        db.session.commit()
        db.session.delete(university)
        db.session.commit()
        return redirect('/posts')
        # except:
        #     return "ERROR"
    else:
        return render_template("unauthorized.html")


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
@login_required
def post_update(id):
    if (current_user.type_user == 'admin'):
        university = University.query.get(id)
        male_female = MaleFemale.query.get(id)
        rank = rank_university.query.get(id)
        if request.method == "POST":
             university.name = request.form['name']
             university.year_construction = request.form['year_construction']
             university.year_repair = request.form['year_repair']
             university.count_student = request.form['count_student']
             university.min_cost = request.form['min_cost']
             university.intro = request.form['intro']
             university.about = request.form['about']

             male_female.count_male = request.form['male']
             male_female.count_female = request.form['female']

             rank.position_qs = request.form['qs']
             rank.position_the = request.form['the']
             rank.position_raex = request.form['raex']
             try:
                 db.session.commit()
                 return redirect('/posts')
             except:
                return redirect('/')
        else:
            return render_template("post_update.html", university=university, male_female=male_female, rank = rank)
    else:
        return render_template("unauthorized.html")


@app.route('/posts/<int:id>/add_speciality', methods=['POST', 'GET'])
@login_required
def add_speciality(id):
    if (current_user.type_user == 'admin'):
        if request.method == "POST":
             name_speciality = request.form['name_speciality']
             number_speciality = request.form['number_speciality']
             rank_speciality = request.form['rank_speciality']

             new_id = Name_speciality.query.order_by(Name_speciality.id_speciality).all().__len__() + 1
             try:
                 new_speciality = Name_speciality(id_speciality = new_id, id_university=id, number_speciality=number_speciality, name_speciality = name_speciality)
                 db.session.add(new_speciality)
                 new_rank = Rank_speciality(id_speciality=new_id, rank_speciality=rank_speciality)
                 db.session.add(new_rank)
             except:
                 return render_template("create_article.html")
             db.session.commit()
             return redirect('/')
        else:
            return render_template("add_speciality.html")
    else:
        return render_template("unauthorized.html")






@manager.unauthorized_handler
def unauthorized():
    return render_template("unauthorized.html")



@app.route('/query', methods=['POST', 'GET'])
def query():
    if request.method == "POST":
        start = request.form.get('start')
        stop = request.form.get('stop')
        if start == None or stop == None:
            return redirect('/')
            if int(start) > int(stop):
                return redirect('/')
        intro = 'Вывести все университеты с Менеджментом в рейтинге от {} до {}'.format(start, stop)
        try:
            text = "select university.id,  university.name, name_speciality.number_speciality, name_speciality.name_speciality, rank_speciality.rank_speciality  \
            from university join name_speciality on university.id = name_speciality.id_university join  rank_speciality on name_speciality.id_speciality = rank_speciality.id_speciality where name_speciality = 'Менеджмент' and rank_speciality.rank_speciality > {} and rank_speciality.rank_speciality < {} order by rank_speciality DESC".format(start, stop)
            cursor.execute(text)
            records = cursor.fetchall()
            need_universities = []
            for record in records:
                id = record[0]
                university = University.query.get(id)
                need_universities.append(university)

            return render_template("posts.html", universities=need_universities,
                                   my_title="Университеты, удовлетворяющие запросу" + "\n '" + intro + "'")
        except:
            return render_template("unauthorized.html")
    else:
        query = db.session.query(Query.id, Query.intro).all()
        try:
            return render_template("query.html", query=query, type_user = current_user.type_user)
        except:
            return render_template("query.html", query=query)

@app.route('/add_query', methods=['POST', 'GET'])
def add_query():
   if (current_user.type_user == 'admin'):
        if request.method == "POST":
            intro = request.form.get('intro')
            full_text = request.form.get('full_text')
            cursor.execute('select id from query ORDER BY ID DESC LIMIT 1')

            new_id = cursor.fetchone()[0] + 1
            query = Query(id=new_id, intro=intro,
                                    full_text=full_text)
            print("re2")
            db.session.add(query)
            db.session.commit()

            print("re3")
            try:
                db.session.add(query)
                db.session.commit()
                print("re4")
                return redirect('/')
            except:
                print("ошибка")
                return render_template("add_query.html")
        else:
            return render_template("add_query.html")
   else:
        return render_template("unauthorized.html")
    # except:
    #     return render_template("query.html")


@app.route('/query/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update_query(id):
    if (current_user.type_user == "admin"):
        query = Query.query.get(id)
        if request.method == "POST":
            query.intro = request.form['intro']
            query.full_text = request.form['full_text']
            db.session.commit()
            return redirect('/query')
        else:
            return render_template("query_update.html", query = query)
    return render_template("unauthorized.html")


@app.route('/query/<int:id>/delete')
@login_required
def delete_query(id):
    query = Query.query.get(id)
    if (current_user.type_user == 'admin'):
        try:
            db.session.delete(query)
            db.session.commit()
            return redirect('/query')
        except:
            return "ERROR"
    return render_template("unauthorized.html")
@app.route('/query/<int:id>/run',  methods=['POST', 'GET'])
@login_required
def query_run(id):
    query = Query.query.get(id)
    text = query.full_text
    cursor.execute(text)
    records = cursor.fetchall()
    need_universities = []
    for record in records:
        id = record[0]
        university = University.query.get(id)
        need_universities.append(university)

    return render_template("posts.html", universities=need_universities, my_title="Университеты, удовлетворяющие запросу" + "\n '" + query.intro + "'")


@app.route('/lk')
@login_required
def lk():
    return render_template("lk.html", user = current_user)


@app.route("/selected")
def selected():
    try:
        need_univer = current_user.university_selected
        need_univer = need_univer.split(';')
        need_univer.pop(len(need_univer) - 1)
        select_univer = []
        for id_univer in need_univer:
            university = University.query.get(id_univer)
            select_univer.append(university)
        return render_template("posts.html", universities=select_univer, my_title="Ваши избранные университеты")
    except:
        return redirect('/')


def close_connection():
    global cursor
    cursor.close()

if __name__ == '__main__':
    app.run(debug= True)