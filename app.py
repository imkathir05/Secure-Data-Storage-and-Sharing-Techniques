import os
from flask import Flask, render_template, url_for, request, session, redirect, send_file, after_this_request
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL

import jinja2
env = jinja2.Environment()
env.globals.update(zip=zip)

import asyenc
import asydec
import base64
import datetime

from flask import Flask
from flask_mail import Mail, Message

app=Flask(__name__)
app.secret_key = 'blockchain'

upload_folder = "uploads/"
if not os.path.exists(upload_folder):
   os.mkdir(upload_folder)

app.config['UPLOAD_FOLDER'] = upload_folder

#configuration of MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'blockchain_logistics'
mysql = MySQL(app)

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'immaslmsms@gmail.com'
app.config['MAIL_PASSWORD'] = 'evtnjqafaycolchh'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/senderreg')
def senderreg():
    return render_template('senderreg.html')

@app.route('/senderlogin')
def senderlogin():
    return render_template('senderlogin.html')

@app.route('/senderregaction', methods=['POST'])
def senderregaction():
    msg=None    
    if request.method == "POST":
        details = request.form
        sname = details['sname']
        semail = details['semail']
        spass = details['spass']
        smno = details['smno']
        saddress = details['saddress']

        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM sender WHERE semail = %s AND smno = %s', (semail, smno))
        result = cursor.fetchone()
        if result:
            msg = 'Sender Already Register...!'
            return render_template('senderreg.html', msg=msg)     
        else:        
            cursor.execute('INSERT INTO sender(sname,semail,spass,smno,saddress) VALUES (%s, %s, %s, %s, %s)', (sname, semail, spass, smno, saddress))
            mysql.connection.commit()
            msg = 'Sender Register Successfully...!'
            return render_template('senderreg.html', msg=msg)                   
    cursor.close() 

@app.route('/senderloginaction', methods=['POST'])
def senderloginaction():
    msg=None    
    if request.method == "POST":
        details = request.form
        semail = details['semail']
        spass = details['spass']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM sender WHERE semail = %s AND spass = %s', (semail, spass))
        result = cursor.fetchone()
        if result:
            session['loggedin'] = True
            session['sid'] = result[0]
            session['sname'] = result[1]   
            return redirect(url_for('senderhome'))
        else:        
            msg = 'Incorrect Sender E-MailID and Password...!'
            return render_template('senderlogin.html', msg=msg)  

@app.route('/senderhome')
def senderhome():
    if 'loggedin' in session:
        return render_template('senderhome.html', sname=session['sname'])
    return redirect(url_for('senderlogin'))   

@app.route('/senderupload')
def senderupload():
    if 'loggedin' in session:
        return render_template('senderupload.html', sid=session['sid'],sname=session['sname'])
    return redirect(url_for('senderlogin'))  

@app.route('/sendersavefile', methods=['GET','POST'])
def sendersavefile():
    msg=None    
    if request.method == 'POST':
        details = request.form
        
        fname = details['fname']
        f = request.files['file']
        
        f.save(os.path.join(app.config['UPLOAD_FOLDER'] ,secure_filename(f.filename)))          
        fpath = os.path.join(app.config['UPLOAD_FOLDER'] ,secure_filename(f.filename))              
        
        file_content = ""
        with open(fpath) as f:
            file_content = f.read()
        
        #Encryption                
        obj = asyenc.Asyencryption()
        encData, publicKey = obj.encryption(file_content.encode())  
        
        pkey =  publicKey.encode("ascii")
        base64_bytes = base64.b64encode(pkey)
        privatekey = base64_bytes.decode("ascii")
        
        #Current Date and Time Get
        now = datetime.datetime.now()        
        cdate = now.strftime("%d-%m-%Y")
        ctime = now.strftime("%I:%M %p")
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM logistics_data WHERE sid = %s AND dname = %s', (session['sid'], fname))
        result = cursor.fetchone()
        
        if result:
            msg = 'Already This Data Added...!'
            return render_template('senderupload.html', msg=msg)     
        else:        
            cursor.execute('INSERT INTO logistics_data(sid,dname,dcontent,hkey,hsign,date,time,adata) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (session['sid'], fname, encData, publicKey, privatekey, cdate, ctime, '0'))
            mysql.connection.commit()
            msg = 'Data Upload Successfully...!'
            return render_template('senderupload.html', msg=msg)             

@app.route('/senderviewfile')
def senderviewfile():
    if 'loggedin' in session:        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM logistics_data WHERE sid = %s', [session['sid']])
        data = cursor.fetchall()
        return render_template('senderviewfile.html', sid=session['sid'], data=data)
    #return redirect(url_for('senderlogin')) 

@app.route('/senderqueryanalysis')
def senderqueryanalysis():
    if 'loggedin' in session:        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM logistics_data WHERE sid = %s', [session['sid']])
        data = cursor.fetchall()
        sname = []        
        sid = [rs[1] for rs in data]  
        for rs in range(len(sid)):           
            cursor.execute('SELECT sname FROM sender WHERE sid = %s',(str(sid[rs])))     
            result = cursor.fetchone() 
            sname.append(result)                              
        cursor.close()  
        #data = {10:30,20:40,30:50,40:70,50:80}  
        #return render_template('senderqueryanalysis.html',data=data) 
        return render_template('senderqueryanalysis.html', sid=session['sid'], data=data, sname=sname, zip=zip)
    return redirect(url_for('senderlogin')) 

@app.route('/senderquerygraph', methods=['POST'])
def senderquerygraph():
    msg=None    
    if request.method == "POST":
        details = request.form
        did = details['did']
        sid = details['sid']
        dname = details['dname']
        adata = int(details['adata'])

        #data = {}  
        #data[dname] = adata
        #data = {dname:adata}
        data = {dname:adata}
        return render_template('senderquerygraph.html', sid=session['sid'], data=data)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('sid', None)
    session.pop('sname', None)
    return redirect(url_for('senderlogin'))   

@app.route('/cloudlogin')
def cloudlogin():
    return render_template('cloudlogin.html')

@app.route('/cloudserveraction', methods=['POST'])
def cloudserveraction():
    msg=None    
    if request.method == "POST":
        details = request.form
        lid = details['lid']
        lpass = details['lpass']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM cloud WHERE lid = %s AND lpass = %s', (lid, lpass))
        result = cursor.fetchone()
        if result:
            session['loggedin'] = True
            session['cid'] = result[0]
            session['cname'] = result[3]   
            return redirect(url_for('cloudhome'))
        else:        
            msg = 'Incorrect Cloud Server ID and Password...!'
            return render_template('cloudlogin.html', msg=msg) 

@app.route('/cloudhome')
def cloudhome():
    if 'loggedin' in session:
        return render_template('cloudhome.html', cname=session['cname'])
    return redirect(url_for('cloudlogin'))    

@app.route('/cloudviewsender')
def cloudviewsender():
    if 'loggedin' in session:        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM sender')
        data = cursor.fetchall()
        return render_template('cloudviewsender.html', cname=session['cname'], data=data)   

@app.route('/cloudviewreciever')
def cloudviewreciever():
    if 'loggedin' in session:        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM reciever')
        data = cursor.fetchall()
        return render_template('cloudviewreciever.html', cname=session['cname'], data=data)  

@app.route('/cloudviewfiles')
def cloudviewfiles():
    if 'loggedin' in session:        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT did, sid, dname, date,time FROM logistics_data')       
        data = cursor.fetchall() 
        sname = []        
        sid = [rs[1] for rs in data]  
        for rs in range(len(sid)):           
            cursor.execute('SELECT sname FROM sender WHERE sid = %s',(str(sid[rs])))     
            result = cursor.fetchone() 
            sname.append(result)      
        cursor.close() 
        return render_template('cloudviewfiles.html', cname=session['cname'], data=data, sname=sname, zip=zip)         

@app.route('/cloudviewfilerequest')
def cloudviewfilerequest():
    if 'loggedin' in session:        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM data_request where reqstatus = %s', ('Send',))       
        data = cursor.fetchall() 

        sname = []        
        sid = [rs[2] for rs in data]  
        for rs in range(len(sid)):           
            cursor.execute('SELECT sname FROM sender WHERE sid = %s',(str(sid[rs])))     
            result = cursor.fetchone() 
            sname.append(result) 
        
        remail = []        
        rid = [rs[4] for rs in data]  
        for rs in range(len(rid)):           
            cursor.execute('SELECT remail FROM reciever WHERE rid = %s',(str(rid[rs])))     
            result1 = cursor.fetchone() 
            remail.append(result1)   

        cursor.close() 
        return render_template('cloudviewfilerequest.html', cname=session['cname'], data=data, sname=sname, remail=remail, zip=zip) 

@app.route('/cloudsendfileaccess', methods=['POST'])
def cloudsendfileaccess(): 
    #if 'loggedin' in session:       
        if request.method == "POST":
            details = request.form
            reqid = details['reqid']
            did = details['did']
            remail = details['remail']
       
            #Current Date and Time Get
            now = datetime.datetime.now()        
            resdate = now.strftime("%d-%m-%Y")
            restime = now.strftime("%I:%M %p")
                  

            did1=''
            dname=''
            skey=''
            cursor1 = mysql.connection.cursor()
            cursor1.execute('SELECT * FROM logistics_data WHERE did = %s', (did))
            result = cursor1.fetchone()        
            if result:   
                did1 = result[0]             
                dname = result[2] 
                skey = result[5]       
            
            #Data_Request Update on Cloud Side
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE data_request SET resdate=%s, restime=%s, skey=%s, reqstatus=%s WHERE reqid=%s', (resdate, restime, skey, 'Response', reqid))
            mysql.connection.commit()
            
            #Mail Send Code
            msg1 = Message('Cloud Server', sender='Blockchain', recipients=[remail])
            msg1.body = 'File ID : '+str(did1)+'\n'+'Data Name : '+dname+'\n'+'Signature Key : '+skey+'\n' 
            mail.send(msg1)            
            return redirect(url_for('cloudhome'))        

@app.route('/clogout')
def clogout():
    session.pop('loggedin', None)
    session.pop('cid', None)
    session.pop('cname', None)
    return redirect(url_for('cloudlogin'))

@app.route('/recieverreg')
def recieverreg():
    return render_template('recieverreg.html')

@app.route('/recieverregaction', methods=['POST'])
def recieverregaction():
    msg=None    
    if request.method == "POST":
        details = request.form
        rname = details['rname']
        remail = details['remail']
        rpass = details['rpass']
        rmno = details['rmno']
        raddress = details['raddress']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM reciever WHERE remail = %s AND rmno = %s', (remail, rmno))
        result = cursor.fetchone()
        if result:
            msg = 'Reciever Already Register...!'
            return render_template('recieverreg.html', msg=msg)     
        else:        
            cursor.execute('INSERT INTO reciever(rname,remail,rpass,rmno,raddress) VALUES (%s, %s, %s, %s, %s)', (rname, remail, rpass, rmno, raddress))
            mysql.connection.commit()
            msg = 'Reciever Register Successfully...!'
            return render_template('recieverreg.html', msg=msg)                       
    cursor.close() 

@app.route('/recieverlogin')
def recieverlogin():
    return render_template('recieverlogin.html')

@app.route('/recieverloginaction', methods=['POST'])
def recieverloginaction():
    msg=None    
    if request.method == "POST":
        details = request.form
        remail = details['remail']
        rpass = details['rpass']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM reciever WHERE remail = %s AND rpass = %s', (remail, rpass))
        result = cursor.fetchone()
        if result:
            session['loggedin'] = True
            session['rid'] = result[0]
            session['rname'] = result[1]   
            session['remail'] = result[2]   
            return redirect(url_for('recieverhome'))
        else:        
            msg = 'Incorrect Reciever E-MailID and Password...!'
            return render_template('recieverlogin.html', msg=msg)  

@app.route('/recieverhome')
def recieverhome():
    if 'loggedin' in session:
        return render_template('recieverhome.html', rname=session['rname'])
    return redirect(url_for('recieverlogin'))  

@app.route('/recieversearchfiles')
def recieversearchfiles():
    if 'loggedin' in session:
        return render_template('recieversearchfiles.html', rname=session['rname'])
    return redirect(url_for('recieverlogin'))  

@app.route('/recieversearchtext', methods=['POST'])
def recieversearchtext():
    msg=None    
    if request.method == "POST":
        details = request.form
        stext = details['stext']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT did, sid, dname, date,time FROM logistics_data WHERE dname LIKE %s', ("%"+stext+"%",))
        data = cursor.fetchall() 
        sname = []        
        sid = [rs[1] for rs in data]  
        for rs in range(len(sid)):           
            cursor.execute('SELECT sname FROM sender WHERE sid = %s',(str(sid[rs])))     
            result = cursor.fetchone() 
            sname.append(result)                              
        cursor.close()  
        return render_template('recieversearchfiles1.html', rid=session['rid'], data=data, sname=sname, zip=zip) 

@app.route('/recieversendrequest', methods=['POST'])
def recieversendrequest():
    msg=None    
    if request.method == "POST":
        details = request.form
        did = details['did']
        sid = details['sid']
        dname = details['dname']
        rid = details['rid']

        #Current Date and Time Get
        now = datetime.datetime.now()        
        reqdate = now.strftime("%d-%m-%Y")
        reqtime = now.strftime("%I:%M %p")
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM data_request WHERE did = %s AND sid = %s AND rid = %s', (did, sid, rid))
        result = cursor.fetchone()
        if result:
            msg = 'Reciever Already This File Requested...!'
            return render_template('recieversearchfiles.html', msg=msg)     
        else:        
            cursor.execute('INSERT INTO data_request(did,sid,dname,rid,reqdate,reqtime,reqstatus) VALUES (%s, %s, %s, %s, %s, %s, %s)', (did, sid, dname, rid, reqdate, reqtime, 'Send'))
            mysql.connection.commit()
            msg = 'Reciever File Request Send Successfully...!'
            return render_template('recieversearchfiles.html', msg=msg)      

@app.route('/recieverdownloadfile')
def recieverdownloadfile():
    if 'loggedin' in session:        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM data_request where rid=%s AND reqstatus=%s', (session['rid'],'Response',))       
        data = cursor.fetchall() 
        sname = []        
        sid = [rs[2] for rs in data]  
        for rs in range(len(sid)):           
            cursor.execute('SELECT sname FROM sender WHERE sid = %s',(str(sid[rs])))     
            result = cursor.fetchone() 
            sname.append(result)   
        cursor.close() 
        return render_template('recieverdownloadfile.html', cname=session['rname'], data=data, sname=sname, zip=zip) 

@app.route('/recieversignatureverification', methods=['POST'])
def recieversignatureverification():       
    if request.method == "POST":
        details = request.form
        did = details['did']

        did1=''
        dname=''
        skey=''
        cursor1 = mysql.connection.cursor()
        cursor1.execute('SELECT * FROM data_request WHERE did = %s AND rid = %s', (did,session['rid']))
        result = cursor1.fetchone()        
        if result:   
            did1 = result[1]             
            dname = result[3] 
            skey = result[9]   

        #Mail Send Code
        msg1 = Message('Cloud Server', sender='Blockchain', recipients=[session['remail']])
        msg1.body = 'File ID : '+str(did1)+'\n'+'Data Name : '+dname+'\n'+'Signature Key : '+skey+'\n' 
        mail.send(msg1)    

        return render_template('recieversignatureverification.html', rid=session['rid'], did=did) 

@app.route('/signatureverification', methods=['POST'])
def signatureverification(): 
    msg=None     
    if request.method == "POST":
        details = request.form
        did = details['did']
        skey = details['skey']
        
        acount=''

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM logistics_data where did=%s AND hsign=%s', (did,skey))       
        result = cursor.fetchone() 
        if result:            
            session['did'] = result[0]
            session['dname'] = result[2]
            session['dcontent'] = result[3]
            session['skey'] = result[5]             
            acount = result[8]

            #Update Access Count
            acount = int(acount) + 1
            cursor1 = mysql.connection.cursor()
            cursor1.execute('UPDATE logistics_data SET adata=%s WHERE did=%s', (acount, did))
            mysql.connection.commit()   

            return redirect(url_for('decryptcontent'))
            #return render_template('recieverviewcontent.html', dname=dname, dcontent=dcontent)  
        else:
            msg = 'Incorrect Signature Key...!'
            return render_template('recieversignatureverification.html', msg=msg, did=did) 

@app.route('/decryptcontent')
def decryptcontent(): 
    did=session['did']
    dname=session['dname']
    dcontent=session['dcontent']
    skey=session['skey']
    
    #Decryption                
    skey1 = skey.encode("ascii")
    skey2 = base64.b64decode(skey1)
    skey3 = skey2.decode("ascii")

    obj = asydec.Asydecryption()
    decdata = obj.decryption(dcontent.encode(),skey3)    

    return render_template('recieverviewcontent.html', dname=dname, decdata=decdata) 

@app.route('/download_file', methods=['POST'])
def download_file():
    if request.method == "POST":
        details = request.form
        dname = details['dname']
        dcontent = details['dcontent']
        #Save File
        fpath = 'uploads/'+str(dname)+'.txt'
        with open(fpath, 'w') as f:
            f.write(str(dcontent))
        print(fpath)        
        #fname = "uploads/Cloud.txt"   
        
        return send_file(fpath, as_attachment=True)        

@app.route('/rlogout')
def rlogout():
    session.pop('loggedin', None)
    session.pop('rid', None)
    session.pop('rname', None)
    return redirect(url_for('recieverlogin'))

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug = True)