from flask import Flask,render_template,url_for,redirect,request,session
import admin_db,string,random
from report import report_bp
import mail
from datetime import timedelta
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import openpyxl
import win32com.client
import pythoncom





admin = Flask(__name__)
admin.secret_key = ''.join(random.choices(string.ascii_letters,k=256))


@admin.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')
    if msg == None:
        return render_template('admin/admin-login.html')
    else:
        return render_template('admin/admin-login.html', msg=msg)
    
    return render_template('admin/admin.html')


@admin.route('/', methods=['POST'])
def login():
    mail = request.form.get('mail') #メールアドレスとパスワードをlogin画面から取得
    password = request.form.get('password')
    
    #ログイン成功処理
    if admin_db.login(mail, password):
        user_information = admin_db.select_account(mail)
        session.permanent = True
        session['user'] = user_information #sessionにキー'user'とバリュー'True'を保存
        admin.permanent_session_lifetime = timedelta(minutes=120) #セッション有効期限設定
        return redirect(url_for('mypage'))
    
    #ログイン失敗処理
    else:
        error = 'ログインに失敗しました。'
        input_data = {'mail':mail,'password':password}
        return render_template('index.html',error=error,data=input_data)

# マイページに遷移する
@admin.route('/mypage', methods=['GET'])
def mypage():
    if 'user' in session:   
        user = session["user"]
        
        return render_template('admin/mypage.html',user=user)
    else:
        return redirect(url_for('index'))



#ログアウト機能
@admin.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('index'))


#新規アカウント登録機能(利用者)
@admin.route('/register_account')
def register_form():
    return render_template('admin/register-teacher.html')

@admin.route('/register_exe', methods=['POST'])
def register_exe():
    

    user_name = request.form.get('user_name')
    mail = request.form.get('mail') 
    password = request.form.get('password')
    
    #入力情報が未入力だった場合の処理
    if user_name == '':
        error = '氏名が未入力です。'
        return render_template('admin/register-teacher.html', error=error,  user_name=user_name, mail=mail, password=password)
    
    if mail == '':
        error = 'メールアドレスが未入力です。'
        return render_template('admin/register-teacher.html', error=error, user_name=user_name, mail=mail, password=password)
    
    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('admin/register-teacher.html', error=error, user_name=user_name, mail=mail, password=password)
    
    
    
    #アカウント登録の結果を処理
    count = admin_db.insert_teacher(user_name,mail,password)
    if count == 1:
        msg = '登録が完了しました。'
        return redirect(url_for('index',msg=msg))
    else:
        error = '登録に失敗しました。既に同じメールアドレスが登録されている可能性があります。'
        return render_template('admin/register-teacher.html',error=error)



#報告書承認
@admin.route('/approve')
def approve_list():
    approve_list = admin_db.approve_list()
    return render_template('admin/approve-list.html',approve_list=approve_list)

@admin.route('/approve_confirm')
def approve_confirm():
    report_id = request.args.get('report_id')
    admin_db.report_approve(report_id)
    return redirect(url_for('approve_end'))

@admin.route('/approve_end',methods=['GET'])
def approve_end():
    return render_template('admin/approve-end.html')
    
    
#報告書詳細表示
@admin.route('/detail')
def report_detail():
    report_id = request.args.get('report_id')
    report_detail = admin_db.report_detail(report_id)
    return render_template('admin/approve-detail.html',approve_detail=report_detail)

#報告書検索
@admin.route('/search')
def search():
    word = request.args.get('word')
    search_list = admin_db.report_search(word)
  
    return render_template('admin/search-result.html',search_list=search_list)

#提出報告書一覧
@admin.route('/report')
def report_list():
    register_list = admin_db.register_list()
    return render_template('admin/report.html',register_list=register_list)

#報告書閲覧
@admin.route('/watch')
def report_watch():
    report_id = request.args.get('report_id')
    report_detail = admin_db.report_detail(report_id)
    
    wb = openpyxl.load_workbook('file\就職試験報告書.xlsx')
    sheet = wb.active
    sheet['AN1'] = f'{report_detail[1]}'
    sheet['D5'] = f'{report_detail[2]}'
    sheet['D7'] = f'{report_detail[3]}'
    sheet['E10'] = f'{report_detail[4]}'
    sheet['AK10'] = f'{report_detail[5]}'
    sheet['E11'] = f'{report_detail[6]}'
    sheet['E12'] = f'{report_detail[7]}'
    sheet['AG12'] = f'{report_detail[8]}'
    sheet['E13'] = f'{report_detail[9]}'
    sheet['AG13'] = f'{report_detail[10]}'
    sheet['I15'] = f'{report_detail[11]}'
    sheet['V15'] = f'{report_detail[12]}'
    sheet['AH15'] = f'{report_detail[13]}'
    sheet['AT15'] = f'{report_detail[14]}'
    sheet['E16'] = f'{report_detail[15]}'
    sheet['I21'] = f'{report_detail[16]}'
    sheet['V21'] = f'{report_detail[17]}'
    sheet['AH21'] = f'{report_detail[18]}'
    sheet['AT21'] = f'{report_detail[19]}'
    sheet['E22'] = f'{report_detail[20]}'
    sheet['I27'] = f'{report_detail[21]}'
    sheet['V27'] = f'{report_detail[22]}'
    sheet['AH27'] = f'{report_detail[23]}'
    sheet['AT27'] = f'{report_detail[24]}'
    sheet['E28'] = f'{report_detail[25]}'
    sheet['E33'] = f'{report_detail[26]}'
    wb.save('file\就職試験報告書.xlsx')
    
    pythoncom.CoInitialize()  # Excelを起動する前にこれを呼び出す
    excel = win32com.client.Dispatch("Excel.Application")
    file = excel.Workbooks.Open('C:\\Users\\takisawa\\Desktop\\就活報告書管理システム\\report_management_system\\file\\就職試験報告書.xlsx')
   
    file.WorkSheets(1).Select()
    #PDF変換
    file.ActiveSheet.ExportAsFixedFormat(0, 'C:\\Users\\takisawa\\Downloads\\就職試験報告書.pdf')

    #エクセルを閉じる
    file.Close()
    excel.Quit()                                                                                                         
    pythoncom.CoUninitialize()  # Excelを終了した後はこれを呼び出す
    
    
    return render_template('admin/watch-report.html',report_detail=report_detail)

#報告書削除
@admin.route('/Delete')
def report_delete():
    report_id = request.args.get('report_id')
   
    return render_template('admin/delete-confirm.html',report_id=report_id)

@admin.route('/Delete_Confrim')
def report_delete2():
    report_id = request.args.get('report_id')
    admin_db.delete_report(report_id)
    return redirect(url_for('report_delete_end'))

@admin.route('/Delete_end',methods=['GET'])
def report_delete_end():
    return render_template('admin/delete-end.html')
    

#メール機能
@admin.route('/send', methods=['POST'])
def send():
    
    report_id = request.form.get('report_id')
    student_id = request.form.get('student_id')
    student_info = admin_db.select_account2(student_id)
    to = student_info[4]
    subject = "報報告書の提出について"
    body = request.form.get('body')
    name = student_info[3]
    
    teacher_info = session['user']
    teacher_name = teacher_info[1]
    teacher_mail = teacher_info[2]
# メール送信
    mail.send_mail(to, subject, body, name, teacher_name, teacher_mail)
    admin_db.resubmit(report_id)
    return redirect(url_for('navigateSend'))

@admin.route('/send', methods=['GET'])
def navigateSend():
    return render_template('admin/resubmit.html')



if __name__ == '__main__':
    admin.run(debug=True)