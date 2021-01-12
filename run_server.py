from flask import *
import sqlite3
from json import JSONEncoder
from types import SimpleNamespace
app = Flask(__name__)
DATABASE = 'userdatabase.db'
app.secret_key = "abc"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def insert_user(name, phone, password, gender):
    con = get_db()
    status = False
    try:
        cur = con.cursor()  
        cur.execute("INSERT INTO users(name,phone,pass,gender)VALUES(?,?,?,?)",(name, phone, password,gender))  
        con.commit()
        status = True
    except:  
        con.rollback()
        status = False
    finally:  
        return status
        
        
        
def checkAdminLogin(phone, password):
    conn = get_db()
    user = query_db('select * from admin_logins where phone = ? AND pass = ?',
                (phone,password), one=True)
    return user
    
    
    
def getAllForms():
    conn = get_db()
    forms = query_db('select * from jobforms')
    
    jobForms = [JobForm] * len(forms)
    
    index = 0;
    for mjobForm in forms:
        #print(mjobForm)
        jobForm = JobForm(mjobForm[0], mjobForm[1], mjobForm[2], mjobForm[3], mjobForm[4], mjobForm[5],
                                mjobForm[6], mjobForm[7], mjobForm[8], mjobForm[9], mjobForm[10], mjobForm[11],
                                    mjobForm[12], mjobForm[13], mjobForm[14], mjobForm[15], mjobForm[16], mjobForm[17], mjobForm[18])
        jobForms[index] = jobForm;
        index += 1
    return jobForms
    
def getAllSubmittForms():
    conn = get_db()
    forms = query_db('select * from jobforms_apply')
    
    jobForms = [JobForm] * len(forms)
    
    index = 0;
    for mjobForm in forms:
        #print(mjobForm)
        jobForm = JobForm(mjobForm[0], mjobForm[1], mjobForm[2], mjobForm[3], mjobForm[4], mjobForm[5],
                                mjobForm[6], mjobForm[7], mjobForm[8], mjobForm[9], mjobForm[10], mjobForm[11],
                                    mjobForm[12], mjobForm[13], mjobForm[14], mjobForm[15], mjobForm[16], mjobForm[17], mjobForm[18])
        jobForms[index] = jobForm;
        index += 1
    return jobForms    
    
    

def delete_form_db(formIndex):
    status = False
    conn = get_db()
    try:
        sql = 'DELETE FROM jobforms WHERE id=?'
        cur = conn.cursor()
        result = cur.execute(sql, (str(formIndex),))
        conn.commit()
    except Exception as e:
        print(e)  
        con.rollback()
        status = False
    finally:  
        return status
        
   
    
    
    

@app.route('/login')
def login():
    return render_template('index.html')


 
@app.route('/')
def default_root():
    return redirect(url_for('login'))
    
    
@app.route('/admin_login',methods = ['POST'])
def admin_login():
    phone=request.form['phone']
    password=request.form['pass']
    user=checkAdminLogin(phone, password)
    if user is None:
       return  "<script>alert('Phone or password did not match.'); window.open('/','_self')</script>"
    else:
        session['admin'] = 'admin'
        session['username'] = user[1]
        return redirect(url_for('admin_account'))
        

    



@app.route('/admin_account',methods = ['GET'])
def admin_account():
    if 'admin' in session:  
        s = session['admin']
        username = session['username']
        return render_template('admin-account.html', username=username) 
        
    else:        
        return render_template('index.html') 
   


       
@app.route('/new_job',methods = ['GET'])
def new_job():
    return render_template('add-new-form.html') 
    
    
    
    
@app.route('/logout',methods = ['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))
    
    
@app.route('/manage_forms',methods = ['GET'])
def manage_forms():
    mjobForms = getAllForms()
    return render_template('manage-all-forms.html',jobForms = mjobForms) 


    
@app.route('/all_application',methods = ['GET'])
def all_application():
    mjobForms = getAllSubmittForms()
    return render_template('all-submitt-forms.html',jobForms = mjobForms) 



@app.route('/delete_forms',methods=['GET', 'POST'])
def delete_form():
    del_index = request.args.get('del_index')
    print("delete index ")
    print(type(del_index))
    print(del_index)
    delete_form_db(del_index)
    
    return redirect(url_for('manage_forms'))
    




@app.route('/downlaod_all_forms_list',methods = ['GET'])
def downlaod_all_forms_list():
    conn = get_db()
    forms = query_db('select * from jobforms')
    return json.dumps(forms)  




class JobForm:
  
    def __init__(self, index, job_title, job_description, first_name, last_name, father_name, mother_name, date_of_birth,
                                permanent_address, corospondence_address, high_school_passing_year, high_school_persentage, 
                                intermideate_passing_year, intermediate_persentage, bachelor_passing_year, bechelor_persentage,
                                pg_passign_year, pg_persentage, marital_status):
                     
        self.index  = index
        self.job_title  = job_title
        self.job_description = job_description
        self.first_name = first_name
        self.last_name = last_name
        self.father_name = father_name
        self.mother_name = mother_name
        self.date_of_birth = date_of_birth
        self.permanent_address = permanent_address
        self.corospondence_address = corospondence_address
        self.high_school_passing_year = high_school_passing_year
        self.high_school_persentage = high_school_persentage
        self.intermideate_passing_year = intermideate_passing_year
        self.intermediate_persentage = intermediate_persentage
        self.bachelor_passing_year = bachelor_passing_year
        self.bechelor_persentage = bechelor_persentage
        self.pg_passign_year = pg_passign_year
        self.pg_persentage = pg_persentage
        self.marital_status = marital_status
      




        
        
        
       


@app.route('/add-new-form-req',methods = ['POST'])
def add_new_form_req():

    NOT_REQUIRE = "NOT_REQUIRE"
    REQUIRED = "REQUIRED"
    job_title  =""
    job_description = ""
    
    first_name = NOT_REQUIRE
    last_name  = NOT_REQUIRE
    father_name = NOT_REQUIRE
    mother_name = NOT_REQUIRE
    date_of_birth = NOT_REQUIRE
    permanent_address  = NOT_REQUIRE
    corospondence_address  = NOT_REQUIRE
    high_school_passing_year = NOT_REQUIRE
    high_school_persentage = NOT_REQUIRE
    intermideate_passing_year  = NOT_REQUIRE
    intermediate_persentage = NOT_REQUIRE
    bachelor_passing_year = NOT_REQUIRE
    bechelor_persentage = NOT_REQUIRE
    pg_passign_year = NOT_REQUIRE
    pg_persentage  = NOT_REQUIRE
    marital_status = NOT_REQUIRE
    
    
    job_title = request.form['title']
    
    job_description = request.form['description']
    
    if 'first_name' in request.form:
        first_name = REQUIRED
        
    if 'last_name' in request.form:
        last_name = REQUIRED
        
    if 'father_name' in request.form:
        father_name = REQUIRED
        
    if 'mother_name' in request.form:
        mother_name = REQUIRED
        
    if 'date_of_birth' in request.form:
        date_of_birth = REQUIRED
        
    if 'permanent_address' in request.form:
        permanent_address = REQUIRED
        
    if 'corospondence_address' in request.form:
        corospondence_address = REQUIRED
        
    if 'high_school_passing_year' in request.form:
        high_school_passing_year = REQUIRED
        
    if 'high_school_persentage' in request.form:
        high_school_persentage = REQUIRED
        
    if 'intermideate_passing_year' in request.form:
        intermideate_passing_year = REQUIRED
        
    if 'intermediate_persentage' in request.form:
        intermediate_persentage = REQUIRED
        
    if 'bachelor_passing_year' in request.form:
        bachelor_passing_year = REQUIRED
        
    if 'bechelor_persentage' in request.form:
        bechelor_persentage = REQUIRED
        
    if 'pg_passign_year' in request.form:
        pg_passign_year = REQUIRED
        
    if 'pg_persentage' in request.form:
        pg_persentage = REQUIRED
    
    
    if 'marital_status' in request.form:
        marital_status = REQUIRED
    
    
    
    jobForm = JobForm(0,job_title, job_description, first_name, last_name, father_name, mother_name, date_of_birth,
                                permanent_address, corospondence_address, high_school_passing_year, high_school_persentage,
                                intermideate_passing_year, intermediate_persentage, bachelor_passing_year, bechelor_persentage,
                                pg_passign_year, pg_persentage, marital_status)
    
    if add_new_job_toDB(jobForm):
        return  "<script>alert('New job added successfuly.'); window.open('/manage_forms','_self')</script>"
    else:
        return  "<script>alert('Fail to add new Job.'); window.open('/manage_forms','_self')</script>"
        







@app.route('/submitt_job_form',methods = ['POST'])
def submitt_job_form():


    NOT_REQUIRE = "NOT_REQUIRE"
    REQUIRED = "REQUIRED"
    job_title  =""
    job_description = ""

    
    first_name = NOT_REQUIRE
    last_name  = NOT_REQUIRE
    father_name = NOT_REQUIRE
    mother_name = NOT_REQUIRE
    date_of_birth = NOT_REQUIRE
    permanent_address  = NOT_REQUIRE
    corospondence_address  = NOT_REQUIRE
    high_school_passing_year = NOT_REQUIRE
    high_school_persentage = NOT_REQUIRE
    intermideate_passing_year  = NOT_REQUIRE
    intermediate_persentage = NOT_REQUIRE
    bachelor_passing_year = NOT_REQUIRE
    bechelor_persentage = NOT_REQUIRE
    pg_passign_year = NOT_REQUIRE
    pg_persentage  = NOT_REQUIRE
    marital_status = NOT_REQUIRE
    
    
    job_title = request.form['job_title']
    job_description = request.form['job_description']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    father_name = request.form['father_name']
    mother_name = request.form['mother_name']
    date_of_birth = request.form['date_of_birth']
    permanent_address = request.form['permanent_address']
    corospondence_address = request.form['corospondence_address']
    mother_name = request.form['mother_name']
    high_school_passing_year = request.form['high_school_passing_year']
    high_school_persentage = request.form['high_school_persentage']
    intermideate_passing_year = request.form['intermideate_passing_year']
    intermediate_persentage = request.form['intermediate_persentage']
    bachelor_passing_year = request.form['bachelor_passing_year']
    bechelor_persentage = request.form['bechelor_persentage']
    pg_passign_year = request.form['pg_passign_year']
    pg_persentage = request.form['pg_persentage']
    marital_status = request.form['marital_status']
    
   
    jobForm = JobForm(0,job_title, job_description, first_name, last_name, father_name, mother_name, date_of_birth,
                                permanent_address, corospondence_address, high_school_passing_year, high_school_persentage,
                                intermideate_passing_year, intermediate_persentage, bachelor_passing_year, bechelor_persentage,
                                pg_passign_year, pg_persentage, marital_status)
    
    if add_job_to_applyDB(jobForm):
        return  "Form submitted successfuly"
    else:
        return  "Fail to submitt from please try again."
        



def add_job_to_applyDB(jobForm):
    con = get_db()
    status = False
    try:
        cur = con.cursor()  
        cur.execute("INSERT INTO jobforms_apply(title, description, firstname, lastname, father_name, mother_name,\
        dob, permanent_address, corospondence_address, high_school_year, high_persent, intermideate_year, intermideate_persent, \
        bachelor_year, bachelor_persent, pg_year, pg_persent, marital_status)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (jobForm.job_title, jobForm.job_description, jobForm.first_name, jobForm.last_name, jobForm.father_name, jobForm.mother_name, 
                jobForm.date_of_birth, jobForm.permanent_address, jobForm.corospondence_address, 
                jobForm.high_school_passing_year, jobForm.high_school_persentage, 
                jobForm.intermideate_passing_year, jobForm.intermediate_persentage,
                jobForm.bachelor_passing_year, jobForm.bechelor_persentage,
                jobForm.pg_passign_year, jobForm.pg_persentage, jobForm.marital_status))
                
        con.commit()
        status = True
    except Exception as e:
        print(e)
        con.rollback()
        status = False
    finally:  
        return status
        
        
        
    
    
    
def add_new_job_toDB(jobForm):
    con = get_db()
    status = False
    try:
        cur = con.cursor()  
        cur.execute("INSERT INTO jobforms(title, description, firstname, lastname, father_name, mother_name,\
        dob, permanent_address, corospondence_address, high_school_year, high_persent, intermideate_year, intermideate_persent, \
        bachelor_year, bachelor_persent, pg_year, pg_persent, marital_status)VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (jobForm.job_title, jobForm.job_description, jobForm.first_name, jobForm.last_name, jobForm.father_name, jobForm.mother_name, 
                jobForm.date_of_birth, jobForm.permanent_address, jobForm.corospondence_address, 
                jobForm.high_school_passing_year, jobForm.high_school_persentage, 
                jobForm.intermideate_passing_year, jobForm.intermediate_persentage,
                jobForm.bachelor_passing_year, jobForm.bechelor_persentage,
                jobForm.pg_passign_year, jobForm.pg_persentage, jobForm.marital_status))
                
        con.commit()
        status = True
    except Exception as e:
        print(e)
        
        con.rollback()
        status = False
    finally:  
        return status
    
    
      
     
   
if __name__ == '__main__':
    app.run(debug = True)