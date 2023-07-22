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
def insert_student(student_number,school_class,user_name,mail,password):
    sql = 'INSERT INTO report_student_account VALUES(default,%s,%s,%s,%s,%s,%s)'
    
    salt = get_salt()
    hashed_password = get_hash(password, salt)
    
    
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (student_number,school_class,user_name,mail, hashed_password, salt))
        count = cursor.rowcount #　更新件数を取得
        connection.commit()
    
    except psycopg2.DatabaseError :
        count = 0
    
    finally :
        cursor.close()
        connection.close()
    
    return count



#学生ログイン
def login(mail, password):
    sql = 'SELECT hashed_password,salt FROM report_student_account WHERE mail = %s'
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
    sql = 'SELECT * FROM report_student_account WHERE mail = %s'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(mail,))
        user_information = cursor.fetchone()
        
    
    finally:
        cursor.close()
        connection.close()
    
    return user_information

def select_class(school_class):
    sql = 'SELECT * FROM report_class WHERE class_id = %s'
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(school_class,))
        user_information = cursor.fetchone()
        
    
    finally:
        cursor.close()
        connection.close()
    
    return user_information


#報告書登録
def register_report(filing_date,result,result_date,company_name,tel,location,name,school_class,occupation,application_method,test1_date,test1_start_time,test1_end_time,test1_division,test1_content,test2_date,test2_start_time,test2_end_time,test2_division,test2_content,test3_date,test3_start_time,test3_end_time,test3_division,test3_content,comment,student_id):
    
    sql = "INSERT INTO report VALUES(default,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1,default)"
    
    
    try :
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql, (filing_date,result,result_date,company_name,tel,location,name,school_class,occupation,application_method,test1_date,test1_start_time,test1_end_time,test1_division,test1_content,test2_date,test2_start_time,test2_end_time,test2_division,test2_content,test3_date,test3_start_time,test3_end_time,test3_division,test3_content,comment,student_id))
        
        count = cursor.rowcount 
        connection.commit()
    
    except psycopg2.DatabaseError :
        count = 0
    
    finally :
        cursor.close()
        connection.close()
    
    return count


#報告書作成一覧取得
def report_list(student_id):
    
    sql = 'SELECT * FROM report WHERE student_id=%s AND NOT resubmit_flag=1'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(student_id,))
        list = cursor.fetchall()
        
    
    finally:
        cursor.close()
        connection.close()
    
    return list

#再提出報告書一覧
def resubmit_list(student_id):
    
    sql = 'SELECT * FROM report WHERE student_id=%s AND resubmit_flag=1'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(student_id,))
        resubmit_list = cursor.fetchall()
        
    
    finally:
        cursor.close()
        connection.close()
    
    return resubmit_list

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

#報告書再提出
def report_resubmit(student_id):
    
    sql = 'UPDATE report SET resubmit_flag=0,register_flag=1 WHERE report_id=%s;'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(student_id))
        count = cursor.rowcount 
        connection.commit()
        
    except psycopg2.DatabaseError :
        count = 0
    
    finally :
        cursor.close()
        connection.close()
    
    return count

#報告書編集
def report_edit(filing_date,result,result_date,company_name,tel,location,name,school_class,occupation,application_method,test1_date,test1_start_time,test1_end_time,test1_division,test1_content,test2_date,test2_start_time,test2_end_time,test2_division,test2_content,test3_date,test3_start_time,test3_end_time,test3_division,test3_content,comment,report_id):
    
    sql = 'UPDATE report SET filing_date=%s,result=%s,result_date=%s,company_name=%s,tel=%s,location=%s,name=%s,school_class=%s,occupation=%s,application_method=%s,test1_date=%s,test1_start_time=%s,test1_end_time=%s,test1_division=%s,test1_content=%s,test2_date=%s,test2_start_time=%s,test2_end_time=%s,test2_division=%s,test2_content=%s,test3_date=%s,test3_start_time=%s,test3_end_time=%s,test3_division=%s,test3_content=%s,comment=%s WHERE report_id=%s;'
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(filing_date,result,result_date,company_name,tel,location,name,school_class,occupation,application_method,test1_date,test1_start_time,test1_end_time,test1_division,test1_content,test2_date,test2_start_time,test2_end_time,test2_division,test2_content,test3_date,test3_start_time,test3_end_time,test3_division,test3_content,comment,report_id))
        count = cursor.rowcount 
        connection.commit()
        
    except psycopg2.DatabaseError :
        count = 0
    
    finally :
        cursor.close()
        connection.close()
    
    return count