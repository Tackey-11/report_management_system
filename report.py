from flask import Blueprint, render_template, request, session,url_for,redirect
import openpyxl,random,string,db
from datetime import timedelta

report_bp = Blueprint('report',__name__,url_prefix='/report')
report_bp.secret_key = ''.join(random.choices(string.ascii_letters,k=256))


#報告書作成
@report_bp.route('/create_report')
def report_create():
    student_class = session['class']
    user = session['user']
    return render_template('report/create-report.html',user=user,student_class=student_class)


@report_bp.route('/report_exe',methods=['POST'])
def report_register():
    
    filing_date = request.form.get('filing_date')
    result = request.form.get('result')
    result_date = request.form.get('result_date')
    company_name = request.form.get('company_name')
    tel = request.form.get('tel')
    location = request.form.get('location')
    name = request.form.get('name')
    
    school_class = request.form.get('school_class')
    occupation = request.form.get('occupation')
    application_method = request.form.get('application_method')
    
    test1_date = request.form.get('test1_date')
    test1_start_time = request.form.get('test1_start_time')
    test1_end_time = request.form.get('test1_end_time')
    test1_division = request.form.get('test1_division')
    test1_content = request.form.get('test1_content')
    
    test2_date = request.form.get('test2_date')
    test2_start_time = request.form.get('test2_start_time')
    test2_end_time = request.form.get('test2_end_time')
    test2_division = request.form.get('test2_division')
    test2_content = request.form.get('test2_content')
    
    test3_date = request.form.get('test3_date')
    test3_start_time = request.form.get('test3_start_time')
    test3_end_time = request.form.get('test3_end_time')
    test3_division = request.form.get('test3_division')
    test3_content = request.form.get('test3_content')
    
    comment = request.form.get('comment')
    
    session.permanent = True
    session['report'] = [filing_date,result,result_date,company_name,tel,location,name,school_class,occupation,application_method,
                         test1_date,test1_start_time,test1_end_time,test1_division,test1_content,
                         test2_date,test2_start_time,test2_end_time,test2_division,test2_content,
                         test3_date,test3_start_time,test3_end_time,test3_division,test3_content,
                         comment]
    report_bp.permanent_session_lifetime = timedelta(minutes=20) 
    
    new_report = session['report']
    return render_template('report/new_report_confirm.html',new_report=new_report)

@report_bp.route('/register_report')
def report_register_confirm():
    report = session['report']
    user = session['user']
    cnt = 0
    
    for x in report:
        if not x:
            report [cnt] = None
            cnt += 1
        else:
            cnt += 1
   
    filing_date = report[0]
    result = report[1]
    result_date = report[2]
    company_name = report[3]
    tel = report[4]
    location = report[5]
    name = report[6]
    
    school_class = report[7]
    occupation = report[8]
    application_method = report[9]
    
    test1_date = report[10]
    test1_start_time = report[11]
    test1_end_time = report[12]
    test1_division = report[13]
    test1_content = report[14]
    
    test2_date = report[15]
    test2_start_time = report[16]
    test2_end_time = report[17]
    test2_division = report[18]
    test2_content = report[19]
    
    test3_date = report[20]
    test3_start_time = report[21]
    test3_end_time = report[22]
    test3_division = report[23]
    test3_content = report[24]
    
    comment = report[25]
    
    student_id = user[0]
    
    
    
    count = db.register_report(filing_date,result,result_date,company_name,tel,location,name,school_class,occupation,application_method,
                         test1_date,test1_start_time,test1_end_time,test1_division,test1_content,
                         test2_date,test2_start_time,test2_end_time,test2_division,test2_content,
                         test3_date,test3_start_time,test3_end_time,test3_division,test3_content,
                         comment,student_id)
    
    if count == 1:
        return redirect(url_for('report.register_report_end'))
    else:
        error = '提出に失敗しました。'
        user = session['user']
        return render_template('report/create-report.html',error=error,user=user)
    
@report_bp.route('/register_report_end', methods=['GET'])
def register_report_end():
    return render_template('report/create-report-end.html')

    # wb = openpyxl.load_workbook('受験申込書&就職試験報告書.xlsx')
    # sheet = wb.active
    # sheet['AN1'] = f'{filing_date}'
    # sheet['D5'] = f'{result}'
    # sheet['D7'] = f'{result_date}'
    # sheet['E10'] = f'{company_name}'
    # sheet['AK10'] = f'{tel}'
    # sheet['E11'] = f'{fr}'
    # sheet['E12'] = f'{name}'
    # sheet['AG12'] = f'{school_class}'
    # sheet['E13'] = f'{occupation}'
    # sheet['AG13'] = f'{application_method}'
    # wb.save('受験申込書&就職試験報告書.xlsx')
    
    
    
#報告書編集
@report_bp.route('/list')
def report_list():
    user = session['user']
    report_list = db.report_list(user[0])
    return render_template('report/list-report.html',report_list=report_list)

@report_bp.route('/resubmit')
def resubmit_list():
    user = session['user']
    resubmit = db.resubmit_list(user[0])
    return render_template('report/resubmit-list.html',resubmit_list=resubmit)


@report_bp.route('/confirm')
def resubmit():
    report_id = request.args.get('report_id')
    return render_template('report/resubmit-confirm.html',report_id=report_id)

@report_bp.route('/resubmit_confirm_end')
def resubmit_end():
    report_id = request.args.get('report_id')
    cont =  db.report_resubmit(report_id)
    return redirect(url_for('report.resubmit_end_page'))

@report_bp.route('/resubmit_end',methods=['GET'])
def resubmit_end_page():
    return render_template('report/resubmit-end.html')
    





@report_bp.route('/detail')
def report_detail():
    report_id = request.args.get('report_id')
    report_detail = db.report_detail(report_id)
    return render_template('report/detail-report.html',report_detail=report_detail)


@report_bp.route('/edit',methods=['POST'])
def report_edit():
    
    report_id = request.form.get('report_id')
    filing_date = request.form.get('filing_date')
    result = request.form.get('result')
    result_date = request.form.get('result_date')
    company_name = request.form.get('company_name')
    tel = request.form.get('tel')
    location = request.form.get('location')
    name = request.form.get('name')
    
    school_class = request.form.get('school_class')
    occupation = request.form.get('occupation')
    application_method = request.form.get('application_method')
    
    test1_date = request.form.get('test1_date')
    test1_start_time = request.form.get('test1_start_time')
    test1_end_time = request.form.get('test1_end_time')
    test1_division = request.form.get('test1_division')
    test1_content = request.form.get('test1_content')
    
    test2_date = request.form.get('test2_date')
    if not test2_date:
        test2_date = None
        
    test2_start_time = request.form.get('test2_start_time')
    if not test2_start_time:
        test2_start_time = None
        
    test2_end_time = request.form.get('test2_end_time')
    if not test2_end_time:
        test2_end_time = None
        
    test2_division = request.form.get('test2_division')
    if not test2_division:
        test2_division = None

    test2_content = request.form.get('test2_content')
    if not test2_content:
        test2_content = None
    
    test3_date = request.form.get('test3_date')
    if not test3_date:
        test3_date = None
    
    test3_start_time = request.form.get('test3_start_time')
    if not test3_start_time:
        test3_start_time = None
    
    test3_end_time = request.form.get('test3_end_time')
    if not test3_end_time:
        test3_end_time = None
    
    test3_division = request.form.get('test3_division')
    if not test3_division:
        test3_division = None
    
    test3_content = request.form.get('test3_content')
    if not test3_content:
        test3_content = None
    
    
    comment = request.form.get('comment')
    
    count = db.report_edit(filing_date,result,result_date,company_name,tel,location,name,school_class,occupation,application_method,
                         test1_date,test1_start_time,test1_end_time,test1_division,test1_content,
                         test2_date,test2_start_time,test2_end_time,test2_division,test2_content,
                         test3_date,test3_start_time,test3_end_time,test3_division,test3_content,
                         comment,report_id)
    
    if count == 1:
        return redirect(url_for('report.report_edit_end'))
    else:
        return redirect(url_for('report.report_list'))

    
@report_bp.route('end',methods=['GET'])
def report_edit_end():
    return render_template('report/edit-end.html')