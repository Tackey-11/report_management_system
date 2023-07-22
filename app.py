from flask import Flask,render_template,url_for,redirect,request,session
import db,string,random
from report import report_bp
import mail
from datetime import timedelta




app = Flask(__name__)
app.register_blueprint(report_bp)


#セッション作成
app.secret_key = ''.join(random.choices(string.ascii_letters,k=256))


# index.htmlへの接続
@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')
    if msg == None:
        return render_template('index.html')
    else:
        return render_template('index.html', msg=msg)
    
    return render_template('index.html')


# @app.route('/')
# def index():
#     return render_template('index.html')

#ログイン機能
@app.route('/', methods=['POST'])
def login():
    mail = request.form.get('mail') #メールアドレスとパスワードをlogin画面から取得
    password = request.form.get('password')
    
    #ログイン成功処理
    if db.login(mail, password):
        user_information = db.select_account(mail)
        session.permanent = True
        session['user'] = user_information #sessionにキー'user'とバリュー'True'を保存
        app.permanent_session_lifetime = timedelta(minutes=120) #セッション有効期限設定
        return redirect(url_for('mypage'))
    
    #ログイン失敗処理
    else:
        error = 'ログインに失敗しました。'
        input_data = {'mail':mail,'password':password}
        return render_template('index.html',error=error,data=input_data)

# マイページに遷移する
@app.route('/mypage', methods=['GET'])
def mypage():
    if 'user' in session:   
        name = session["user"]
        
        student_class = db.select_class(name[2])
        session.permanent = True
        session['class'] = student_class
        app.permanent_session_lifetime = timedelta(minutes=120)
    
        
        return render_template('mypage.html',name=name)
    else:
        return redirect(url_for('index'))



#ログアウト機能
@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('index'))


#新規アカウント登録機能(利用者)
@app.route('/register_account')
def register_form():
    return render_template('register-student.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    
    student_number = request.form.get('student_number') #アカウント登録画面から入力情報を取得
    school_class = request.form.get('school_class')
    user_name = request.form.get('user_name')
    mail = request.form.get('mail') 
    password = request.form.get('password')
    
    #入力情報が未入力だった場合の処理
    if student_number == '':
        error = '学籍番号が未入力です。'
        return render_template('register-student.html', error=error, student_number=student_number, school_class=school_class, user_name=user_name, mail=mail, password=password)
    
    if school_class == '':
        error = 'クラスが未入力です。'
        return render_template('register-student.html', error=error, student_number=student_number, school_class=school_class, user_name=user_name, mail=mail, password=password)
    
    if user_name == '':
        error = '氏名が未入力です。'
        return render_template('register-student.html', error=error, student_number=student_number, school_class=school_class, user_name=user_name, mail=mail, password=password)
    
    if mail == '':
        error = 'メールアドレスが未入力です。'
        return render_template('register-student.html', error=error, student_number=student_number, school_class=school_class, user_name=user_name, mail=mail, password=password)
    
    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('register-student.html', error=error, student_number=student_number, school_class=school_class, user_name=user_name, mail=mail, password=password)
    
    
    
    #アカウント登録の結果を処理
    count = db.insert_student(student_number,school_class,user_name,mail,password)
    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index',msg=msg))
    else:
        error = '登録に失敗しました。既に同じメールアドレスが登録されている可能性があります。'
        return render_template('register-student.html',error=error)
    
# メール送信
@app.route('/send',methods=['POST'])
def send():
    to = request.form.get('to')
    subject = request.form.get('subject')
    body = request.form.get('body')

    mail.send_mail(to, subject, body)
    
    return redirect(url_for('navigateSend'))

@app.route('/send', methods=['GET'])
def navigateSend():
    return render_template('send.html')

if __name__ == '__main__':
    app.run(debug=True)