import os,psycopg2,string,random,hashlib
from flask import Flask,session

#データベース接続
def get_connection():
    url = os.environ['DATABASE_URL']
    conneciton = psycopg2.connect(url)
    return conneciton

#ソルトの取得
def get_salt():
    charset = string.ascii_letters + string.digits
    
    salt = ''.join(random.choices(charset, k=30))
    return salt

#ソルトを使ったパスワードのハッシュ化
def get_hash(password,salt):
    b_pw = bytes(password, 'utf-8')
    b_salt = bytes(salt, 'utf-8')

    hashed_password = hashlib.pbkdf2_hmac('sha256', b_pw, b_salt, 1246).hex()
    return hashed_password

#新規アカウント登録
def insert_teacher(user_name,mail,password):
    sql = 'INSERT INTO report_teacher_account VALUES(default,%s,%s,%s,%s)'
    
    salt = get_salt()
    hashed_password = get_hash(password, salt)
    
    
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (user_name,mail, hashed_password, salt))
        count = cursor.rowcount #　更新件数を取得
        connection.commit()
    
    except psycopg2.DatabaseError :
        count = 0
    
    finally :
        cursor.close()
        connection.close()
    
    return count



#ログイン
def login(mail, password):
    sql = 'SELECT hashed_password,salt FROM report_teacher_account WHERE mail = %s'
    flg = False
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (mail,))
        user = cursor.fetchone()
        
        if user != None:
            salt = user[1]
            hashed_password = get_hash(password, salt)
            
            if hashed_password == user[0]:
                flg = True
                
    except psycopg2.DatabaseError:
        flg = False
    finally:
        cursor.close()
        connection.close()
        
    return flg


def select_account(mail):
    sql = 'SELECT * FROM report_teacher_account WHERE mail = %s'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(mail,))
        user_information = cursor.fetchone()
        
    
    finally:
        cursor.close()
        connection.close()
    
    return user_information

#student_idから学生アカウント情報取得
def select_account2(student_id):
    sql = 'SELECT * FROM report_student_account WHERE student_id = %s'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(student_id,))
        student_information = cursor.fetchone()
        
    
    finally:
        cursor.close()
        connection.close()
    
    return student_information


#報告書承認一覧
def approve_list():
    
    sql = 'SELECT * FROM report WHERE register_flag=1'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,)
        approve_list = cursor.fetchall()
        
    
    finally:
        cursor.close()
        connection.close()
    
    return approve_list

#報告書詳細取得
def report_detail(report_id):
    
    sql = 'SELECT * FROM report WHERE report_id=%s'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(report_id,))
        report_detail = cursor.fetchone()
        
    finally:
        cursor.close()
        connection.close()
        
    return report_detail

#報告書承認
def report_approve(report_id):
    sql = 'UPDATE report SET register_flag=2 WHERE report_id=%s;'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(report_id))
        count = cursor.rowcount 
        connection.commit()
        
    except psycopg2.DatabaseError :
        count = 0
    
    finally :
        cursor.close()
        connection.close()
    
    return count

#報告書再提出
def resubmit(report_id):
    sql = 'UPDATE report SET register_flag=0,resubmit_flag=1 WHERE report_id=%s;'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(report_id))
        count = cursor.rowcount 
        connection.commit()
        
    except psycopg2.DatabaseError :
        count = 0
    
    finally :
        cursor.close()
        connection.close()
    
    return count

#報告書検索
def report_search(keyword):
    sql = 'SELECT * FROM report WHERE company_name LIKE %s ORDER BY company_name;'
    
    
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
       
        key = f'%{keyword}%'
        cursor.execute(sql,(key,))
       
        search_list = cursor.fetchall()
        
    
    finally:
        cursor.close()
        connection.close()

    return search_list

#登録報告書一覧
def register_list():
    sql = 'SELECT * FROM report WHERE register_flag=2 ORDER BY company_name;'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,)
        register_list = cursor.fetchall()
        
    
    finally:
        cursor.close()
        connection.close()
    
    return register_list

#報告書削除
def delete_report(report_id):
    sql = 'DELETE FROM report WHERE report_id=%s;'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(report_id))
        count = cursor.rowcount 
        connection.commit()
        
    except psycopg2.DatabaseError :
        count = 0
    
    finally :
        cursor.close()
        connection.close()
    
    return count
