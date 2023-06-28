from flask import Flask,render_template,url_for,redirect,request,session
import db,string,random
import mail
from datetime import timedelta

app = Flask(__name__)
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
        session['user'] = True #sessionにキー'user'とバリュー'True'を保存
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=60) #セッション有効期限設定
        return redirect(url_for('mypage'))
    
    #ログイン失敗処理
    else:
        error = 'ログインに失敗しました。'
        input_data = {'mail':mail,'password':password}
        return render_template('index.html',error=error,data=input_data)


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
    mail = request.form.get('mail') #アカウント登録画面から入力情報を取得
    password = request.form.get('password')
    
    #入力情報が未入力だった場合の処理
    if mail == '':
        error = 'メールアドレスが未入力です。'
        return render_template('register-account.html', error=error, mail=mail, password=password)
    
    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('register-account.html',error=error,mail=mail,password=password)
    
    #アカウント登録の結果を処理
    count = db.insert_user(mail,password)
    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index',msg=msg))
    else:
        error = '登録に失敗しました。'
        return render_template('register-account.html',error=error)
    
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