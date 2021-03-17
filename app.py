from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
    flash,
    abort,
    app
)
import os
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.utils import secure_filename
from flask_apscheduler import APScheduler
from skpy import Skype
import json
import html
import pandas as pd
import numpy as np
import re

countries_dict = {"AF": "Afghanistan", "AL": "Albania", "DZ": "Algeria", "AX": "Aland Islands", "AS": "American Samoa", "AI": "Anguilla", "AD": "Andorra", "AO": "Angola", "AN": "Antilles - Netherlands ", "AG": "Antigua and Barbuda", "AQ": "Antarctica", "AR": "Argentina", "AM": "Armenia", "AU": "Australia", "AT": "Austria", "AW": "Aruba", "AZ": "Azerbaijan", "BA": "Bosnia and Herzegovina", "BB": "Barbados", "BD": "Bangladesh", "BE": "Belgium", "BF": "Burkina Faso", "BG": "Bulgaria", "BH": "Bahrain", "BI": "Burundi", "BJ": "Benin", "BM": "Bermuda", "BN": "Brunei Darussalam", "BO": "Bolivia", "BR": "Brazil", "BS": "Bahamas", "BT": "Bhutan", "BV": "Bouvet Island", "BW": "Botswana", "BV": "Belarus", "BZ": "Belize", "KH": "Cambodia", "CM": "Cameroon", "CA": "Canada", "CV": "Cape Verde", "CF": "Central African Republic", "TD": "Chad", "CL": "Chile", "CN": "China", "CX": "Christmas Island", "CC": "Cocos (Keeling) Islands", "CO": "Colombia", "CG": "Congo", "CI": "Cote D'Ivoire (Ivory Coast)", "CK": "Cook Islands", "CR": "Costa Rica", "HR": "Croatia (Hrvatska)", "CU": "Cuba", "CY": "Cyprus", "CZ": "Czech Republic", "CD": "Democratic Republic of the Congo", "DJ": "Djibouti", "DK": "Denmark", "DM": "Dominica", "DO": "Dominican Republic", "EC": "Ecuador", "EG": "Egypt", "SV": "El Salvador", "TP": "East Timor", "EE": "Estonia", "GQ": "Equatorial Guinea", "ER": "Eritrea", "ET": "Ethiopia", "FI": "Finland", "FJ": "Fiji", "FK": "Falkland Islands (Malvinas)", "FM": "Federated States of Micronesia", "FO": "Faroe Islands", "FR": "France", "FX": "France, Metropolitan", "GF": "French Guiana", "PF": "French Polynesia", "GA": "Gabon", "GM": "Gambia", "DE": "Germany", "GH": "Ghana", "GI": "Gibraltar", "GB": "Great Britain (UK)", "GD": "Grenada", "GE": "Georgia", "GR": "Greece", "GL": "Greenland", "GN": "Guinea", "GP": "Guadeloupe", "GS": "S. Georgia and S. Sandwich Islands", "GT": "Guatemala", "GU": "Guam", "GW": "Guinea-Bissau", "GY": "Guyana", "HK": "Hong Kong", "HM": "Heard Island and McDonald Islands", "HN": "Honduras", "HT": "Haiti", "HU": "Hungary", "ID": "Indonesia", "IE": "Ireland", "IL": "Israel", "IN": "India", "IO": "British Indian Ocean Territory", "IQ": "Iraq", "IR": "Iran", "IT": "Italy", "JM": "Jamaica", "JO": "Jordan", "JP": "Japan", "KE": "Kenya", "KG": "Kyrgyzstan", "KI": "Kiribati", "KM": "Comoros", "KN": "Saint Kitts and Nevis", "KP": "Korea (North)", "KR": "Korea (South)", "KW": "Kuwait", "KY": "Cayman Islands", "KZ": "Kazakhstan", "LA": "Laos", "LB": "Lebanon", "LC": "Saint Lucia", "LI": "Liechtenstein", "LK": "Sri Lanka", "LR": "Liberia", "LS": "Lesotho", "LT": "Lithuania", "LU": "Luxembourg", "LV": "Latvia", "LY": "Libya", "MK": "Macedonia", "MO": "Macao", "MG": "Madagascar", "MY": "Malaysia", "ML": "Mali", "MW": "Malawi", "MR": "Mauritania", "MH": "Marshall Islands", "MQ": "Martinique", "MU": "Mauritius", "YT": "Mayotte", "MT": "Malta", "MX": "Mexico", "MA": "Morocco", "MC": "Monaco", "MD": "Moldova", "MN": "Mongolia", "MM": "Myanmar", "MP": "Northern Mariana Islands", "MS": "Montserrat", "MV": "Maldives", "MZ": "Mozambique", "NA": "Namibia", "NC": "New Caledonia", "NE": "Niger", "NF": "Norfolk Island", "NG": "Nigeria", "NI": "Nicaragua", "NL": "Netherlands", "NO": "Norway", "NP": "Nepal", "NR": "Nauru", "NU": "Niue", "NZ": "New Zealand (Aotearoa)", "OM": "Oman", "PA": "Panama", "PE": "Peru", "PG": "Papua New Guinea", "PH": "Philippines", "PK": "Pakistan", "PL": "Poland", "PM": "Saint Pierre and Miquelon", "CS": "Serbia and Montenegro", "PN": "Pitcairn", "PR": "Puerto Rico", "PS": "Palestinian Territory", "PT": "Portugal", "PW": "Palau", "PY": "Paraguay", "QA": "Qatar", "RE": "Reunion", "RO": "Romania", "RU": "Russian Federation", "RW": "Rwanda", "SA": "Saudi Arabia", "WS": "Samoa", "SH": "Saint Helena", "VC": "Saint Vincent and the Grenadines", "SM": "San Marino", "ST": "Sao Tome and Principe", "SN": "Senegal", "SC": "Seychelles", "SL": "Sierra Leone", "SG": "Singapore", "SK": "Slovakia", "SI": "Slovenia", "SB": "Solomon Islands", "SO": "Somalia", "ZA": "South Africa", "ES": "Spain", "SD": "Sudan", "SR": "Suriname", "SJ": "Svalbard and Jan Mayen", "SE": "Sweden", "CH": "Switzerland", "SY": "Syria", "SU": "USSR (former)", "SZ": "Swaziland", "TW": "Taiwan", "TZ": "Tanzania", "TJ": "Tajikistan", "TH": "Thailand", "TL": "Timor-Leste", "TG": "Togo", "TK": "Tokelau", "TO": "Tonga", "TT": "Trinidad and Tobago", "TN": "Tunisia", "TR": "Turkey", "TM": "Turkmenistan", "TC": "Turks and Caicos Islands", "TV": "Tuvalu", "UA": "Ukraine", "UG": "Uganda", "AE": "United Arab Emirates", "UK": "United Kingdom", "US": "United States", "UM": "United States Minor Outlying Islands", "UY": "Uruguay", "UZ": "Uzbekistan", "VU": "Vanuatu", "VA": "Vatican City State", "VE": "Venezuela", "VG": "Virgin Islands (British)", "VI": "Virgin Islands (U.S.)", "VN": "Viet Nam", "WF": "Wallis and Futuna", "EH": "Western Sahara", "YE": "Yemen", "YU": "Yugoslavia (former)", "ZM": "Zambia", "ZR": "Zaire (former)", "ZW": "Zimbabwe"}

app = Flask(__name__)

scheduler = APScheduler()
scheduler.daemonic = False
scheduler.init_app(app)
if not scheduler.running:
    scheduler.start()

app.secret_key = 'secret'

app.config['MYSQL_HOST'] = 'mysql3000.mochahost.com'
app.config['MYSQL_USER'] = 'ivision1_ivision'
app.config['MYSQL_PASSWORD'] = 'iVision'
app.config['MYSQL_DB'] = 'ivision1_ivisions_b2bai'

mysql = MySQL(app)
app.config['UPLOAD_PATH'] = 'uploads/'

first_time = True

def scheduledFunction():
    try:
        print("The scheduled jobs started...")
        scheduler.add_job(id='scheduled task', replace_existing=True, func=update_conversation,
                          trigger='interval', minutes=60)
    except Exception as e:
        print("Exception : ", str(e))
        
@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.form.get('lg_out'):
        logout()
    if session.get('ivisions_user'):
        return redirect(url_for('dashboard'))
    else:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM login WHERE username = % s AND password = % s', (username, password,))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['ivisions_user'] = username
                session.permanent = True
                session.modified = True
                return redirect(url_for('dashboard'))
        return render_template('login.html')

def logout():
    session.clear()
    flash('Logged out.')
    return redirect(url_for('login'))

@app.route('/group1', methods=['GET', 'POST'])
def group1():
    try:
        if not session.get('ivisions_user'):
            return redirect(url_for('login'))

        if request.method == 'POST':
            sk = Skype(tokenFile=".tokens_File")
            logged_id = str(sk).split('UserId:')[1].strip()
            update_cursor = mysql.connection.cursor()
            sql_update_query = ""
            if request.form.get('tb_row'):
                tb_row = request.form.get('tb_row')
                sk_id, display_name, manufacture, p_type, supplier = tb_row.split('-:::-')
                if sk_id and display_name and manufacture and p_type and supplier:
                    if supplier == 'client':
                        sql_update_query = 'UPDATE client SET type=%s WHERE skype_id=%s AND manufacturer=%s AND logged_in_user=%s'
                    elif supplier == 'vendor':
                        sql_update_query = 'UPDATE vendor SET type=%s WHERE skype_id=%s AND manufacturer=%s AND logged_in_user=%s'

            update_cursor.execute(sql_update_query, (p_type, sk_id, manufacture, logged_id))
            mysql.connection.commit()
            return render_template('group.html', sk_user=session['skype_id'])

    except Exception as e:
        print(str(e))

@app.route('/group', methods=['GET', 'POST'])
def group():
    try:
        if not session.get('ivisions_user'):
            return redirect(url_for('login'))

        if request.method == 'POST':
            sk = Skype(tokenFile=".tokens_File")
            logged_id = str(sk).split('UserId:')[1].strip()
            cursor = mysql.connection.cursor()
            sql_query = ""
            if request.form.get('supplier_selected'):
                selected_supplier = request.form.get('supplier_selected')
                if selected_supplier == 'client':
                    sql_query = 'SELECT DISTINCT(c.skype_id), ci.display_name, c.manufacturer' \
                                ' FROM client c INNER JOIN contact_info ci' \
                                ' ON c.skype_id = ci.skype_id' \
                                ' WHERE c.type = "" AND logged_in_user=%s'
                elif selected_supplier == 'vendor':
                    sql_query = 'SELECT DISTINCT(v.skype_id), ci.display_name, v.manufacturer' \
                                ' FROM vendor v INNER JOIN contact_info ci' \
                                ' ON v.skype_id = ci.skype_id' \
                                ' WHERE v.type = "" AND logged_in_user=%s'

            cursor.execute(sql_query, (logged_id,))
            data = cursor.fetchall()
            mysql.connection.commit()

            return render_template('group.html', sk_user=session['skype_id'], data=data, supplier_=selected_supplier)
        else:
            return render_template('group.html', sk_user=session['skype_id'])

    except Exception as e:
        print(str(e))

@app.route('/dashboard')
def dashboard(value=None):
    try:
        if not session.get('ivisions_user'):
            return redirect(url_for('login'))

        if session.get('skype_id'):
            global first_time
            if first_time:
                first_time = False
            scheduledFunction()
            # classification()
            return render_template('dashboard.html', sk_user=session['skype_id'])
        else:
            return render_template('dashboard.html')

    except Exception as e:
        print("Exception : ", str(e))

@app.route('/ai', methods=['GET', 'POST'])
def ai():
    try:
        if not session.get('ivisions_user'):
            return redirect(url_for('login'))

        if session.get('skype_id'):
            return render_template('dashboard.html', sk_user=session['skype_id'])
        else:
            if request.method == 'POST':
                email_id = request.form['uname']
                pwd = request.form['psw']
                try:
                    sk = Skype(email_id, pwd, ".tokens_File")
                    if sk:
                        user_id = str(sk.user)
                        user_id = user_id.split("Name")[0].split(":")[1].strip()
                        user_id_chat = "8:"+user_id
                        session['user_id_chat'] = user_id_chat
                        session['skype_id'] = email_id
                        session['skype_pwd'] = pwd
                        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                        cursor.execute('SELECT * FROM ai_login WHERE login_user = % s AND password = % s', (email_id, pwd,))
                        account = cursor.fetchone()
                        if not account:
                            cursor1 = mysql.connection.cursor()
                            cursor1.execute('INSERT INTO ai_login (login_user, password) VALUES (%s, %s) ', (email_id, pwd,))
                            mysql.connection.commit()
                            return redirect(url_for('upload_json'))
                        elif not account['json_file']:
                            return redirect(url_for('upload_json'))
                        elif not account['csv_file']:
                            return redirect(url_for('upload'))
                        else:
                            return render_template('dashboard.html', sk_user=session['skype_id'])

                except Exception as e:
                    print(e)

            return render_template('ai.html')

    except Exception as e:
        print("Exception : ", str(e))

@app.route('/upload',methods=['GET', 'POST'])
def upload():
    try:
        if not session.get('ivisions_user'):
            return redirect(url_for('login'))

        if session.get('skype_id'):
            if request.method == 'POST':
                sk = Skype(tokenFile=".tokens_File")
                sk_id = str(sk).split('UserId:')[1].strip()
                uploaded_file = request.files['selectFiles1']
                filename = secure_filename(uploaded_file.filename)
                filename_ = filename.split('.')[0]
                filename_ += '_' + sk_id + '.csv'
                if filename != '':
                    file_ext = os.path.splitext(filename)[1]
                    uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('SELECT * FROM ai_login WHERE login_user = % s AND password = % s', (session['skype_id'], session['skype_pwd'],))
                    account = cursor.fetchone()
                    if not account['csv_file']:
                        cursor1 = mysql.connection.cursor()
                        cursor1.execute('UPDATE ai_login SET csv_file=%s WHERE login_user=%s AND password=%s ', (filename_, session['skype_id'], session['skype_pwd'],))
                        mysql.connection.commit()

                    data_csv = pd.DataFrame()
                    data_contacts = pd.DataFrame()
                    data_csv = pd.read_csv(os.path.join(app.config['UPLOAD_PATH'], filename))
                    data_csv = data_csv.query("type == 'Skype' & blocked == False")

                    data_contacts['skype_id'] = data_csv['id']
                    data_contacts['display_name'] = data_csv['display_name']
                    data_contacts['gender'] = data_csv['profile.gender']
                    data_contacts['country'] = data_csv['profile.locations[0].country'].str.lower()
                    data_contacts['city'] = data_csv['profile.locations[0].city']
                    data_contacts['state'] = data_csv['profile.locations[0].state']
                    data_contacts['firstname'] = data_csv['profile.name.first']
                    data_contacts['surname'] = data_csv['profile.name.surname']
                    data_contacts['mobile_no'] = data_csv['profile.phones[0].number']
                    data_contacts['office_no'] = data_csv['profile.phones[1].number']
                    data_contacts['website'] = data_csv['profile.website']
                    data_contacts['added_date'] = data_csv['creation_time']
                    data_contacts['logged_in_user'] = sk_id

                    data_contacts = data_contacts.fillna("Null")

                    from datetime import date, timedelta
                    today_ = date.today()

                    cursor = mysql.connection.cursor()
                    cursor.execute(
                        'SELECT imported_date FROM contact_info WHERE logged_in_user = %s ORDER BY imported_date DESC',
                        (sk_id,))
                    last_imported_date = cursor.fetchone()
                    if not last_imported_date:
                        data_contacts['imported_date'] = today_
                        sql_insert = "INSERT INTO contact_info (skype_id, display_name, gender, country, city, state, firstname, surname, mobile_no, office_no, website, added_date, imported_date, logged_in_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        cursor.executemany(sql_insert, list(zip(data_contacts['skype_id'],
                                                                data_contacts['display_name'],
                                                                data_contacts['gender'],
                                                                data_contacts['country'],
                                                                data_contacts['city'],
                                                                data_contacts['state'],
                                                                data_contacts['firstname'],
                                                                data_contacts['surname'],
                                                                data_contacts['mobile_no'],
                                                                data_contacts['office_no'],
                                                                data_contacts['website'],
                                                                data_contacts['added_date'],
                                                                data_contacts['imported_date'],
                                                                data_contacts['logged_in_user'])))
                        mysql.connection.commit()
                    else:
                        last_imported_date = last_imported_date[0].strftime("%Y-%m-%d")
                        new_contacts_df = data_contacts.loc[data_contacts['added_date'] > last_imported_date]
                        new_contacts_df['imported_date'] = today_
                        print(new_contacts_df.head(10))
                        if new_contacts_df.shape[0] > 0:
                            sql_insert = "INSERT INTO contact_info (skype_id, display_name, gender, country, city, state, firstname, surname, mobile_no, office_no, website, added_date, imported_date, logged_in_user) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            cursor.executemany(sql_insert, list(zip(new_contacts_df['skype_id'],
                                                                    new_contacts_df['display_name'],
                                                                    new_contacts_df['gender'],
                                                                    new_contacts_df['country'],
                                                                    new_contacts_df['city'],
                                                                    new_contacts_df['state'],
                                                                    new_contacts_df['firstname'],
                                                                    new_contacts_df['surname'],
                                                                    new_contacts_df['mobile_no'],
                                                                    new_contacts_df['office_no'],
                                                                    new_contacts_df['website'],
                                                                    new_contacts_df['added_date'],
                                                                    new_contacts_df['imported_date'],
                                                                    new_contacts_df['logged_in_user'])))
                            mysql.connection.commit()

                    update_contacts(filename)             # from outer python file
                    return render_template('dashboard.html', sk_user=session['skype_id'])

            return render_template('upload_csv.html', sk_user=session['skype_id'])
        else:
            return render_template('ai.html')

    except Exception as e:
        print("Exception : ", str(e))
    
@app.route('/upload_json',methods=['GET', 'POST'])
def upload_json():
    try:
        if not session.get('ivisions_user'):
            return redirect(url_for('login'))

        if request.method == 'POST':
            uploaded_file = request.files['selectFiles']
            filename = secure_filename(uploaded_file.filename)

            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                export_date = ""
                with open(os.path.join(app.config['UPLOAD_PATH'], filename)) as f:
                    data = json.load(f)
                    export_date = data['exportDate'].split("T")[0]
                filename_ = filename.split('.')[0]

                sk = Skype(tokenFile=".tokens_File")
                sk_id = str(sk).split('UserId:')[1].strip()

                # filename_ += '_'+session['skype_id'].split('@')[0]
                filename_ += '_' + sk_id
                filename_ += '.json'

                cursor = mysql.connection.cursor()
                cursor.execute('UPDATE ai_login SET json_file=%s,uploaded_json=%s WHERE login_user=%s AND password=%s ', (filename_, export_date, session['skype_id'], session['skype_pwd'],))
                mysql.connection.commit()
                read_conversation(filename)
                return render_template('dashboard.html', sk_user=session['skype_id'])
        return render_template('upload_json_onetime.html', sk_user=session['skype_id'])
    except Exception as e:
        print("Exception : ", str(e))

@app.route('/add-country', methods=['GET', 'POST'])
def add_country():
    try:
        if not session.get('ivisions_user'):
            return redirect(url_for('login'))

        if session['skype_id']:
            sk = Skype(tokenFile=".tokens_File")
            logged_id = str(sk).split('UserId:')[1].strip()
            
            if request.method == 'POST':
                tb_row = request.form.get('tb_row')
                sk_id, display_name, get_country = tb_row.split('-:::-')
                # print(sk_id, display_name, get_country.lower())
                update_cursor = mysql.connection.cursor()
                update_cursor.execute('UPDATE contact_info SET country=%s WHERE skype_id=%s AND display_name=%s AND logged_in_user=%s',
                               (get_country.lower(), sk_id, display_name, logged_id,))
                mysql.connection.commit()

            cursor = mysql.connection.cursor()
            cursor.execute('SELECT skype_id, display_name FROM contact_info WHERE country LIKE "Null" AND logged_in_user=%s', (logged_id,))
            data = cursor.fetchall()
            mysql.connection.commit()

            return render_template('add-country.html', sk_user=session['skype_id'], countries=countries_dict, data=data)
        else:
            logout()

    except Exception as e:
        print(str(e))

@app.route('/classify-contacts', methods=['GET', 'POST'])
def unclassified():
    try:
        if not session.get('ivisions_user'):
            return redirect(url_for('login'))

        if session['skype_id']:
            sk_id = session['skype_id']
            sk_pwd = session['skype_pwd']
            sk = Skype(sk_id, sk_pwd)

            sk_token = Skype(tokenFile=".tokens_File")
            sk_token_id = str(sk_token).split('UserId:')[1].strip()
            
            if request.method == 'POST':
                get_skype_id = request.form.get('sk_id_selected')
                supplier = request.form.get('supplier_selected').lower()
                manufacture = request.form.get('manufact_selected')
                p_type = request.form.get('type_selected')
                
                cursor_ = mysql.connection.cursor()
                if supplier == "client":
                    if manufacture and p_type:
                       cursor_.execute('INSERT INTO client (skype_id, manufacturer, type, logged_in_user) VALUES (%s, %s, %s, %s)',
                                       (get_skype_id, manufacture, p_type, sk_token_id,))
                    elif manufacture:
                        cursor_.execute('INSERT INTO client (skype_id, manufacturer, logged_in_user) VALUES (%s, %s, %s)',
                            (get_skype_id, manufacture, sk_token_id,))

                elif supplier == "vendor":
                    if manufacture and p_type:
                       cursor_.execute('INSERT INTO vendor (skype_id, manufacturer, type, logged_in_user) VALUES (%s, %s, %s, %s)',
                                       (get_skype_id, manufacture, p_type, sk_token_id,))
                    elif manufacture:
                        cursor_.execute('INSERT INTO vendor (skype_id, manufacturer, logged_in_user) VALUES (%s, %s, %s)',
                            (get_skype_id, manufacture, sk_token_id,))

                elif supplier == "vendorclient":
                    if manufacture and p_type:
                       cursor_.execute('INSERT INTO vendor (skype_id, manufacturer, type, logged_in_user) VALUES (%s, %s, %s, %s)',
                                       (get_skype_id, manufacture, p_type, sk_token_id,))
                       mysql.connection.commit()
                       cursor_.execute('INSERT INTO client (skype_id, manufacturer, type, logged_in_user) VALUES (%s, %s, %s, %s)',
                           (get_skype_id, manufacture, p_type, sk_token_id,))
                    elif manufacture:
                        cursor_.execute('INSERT INTO vendor (skype_id, manufacturer, logged_in_user) VALUES (%s, %s, %s)',
                            (get_skype_id, manufacture, sk_token_id,))
                        mysql.connection.commit()
                        cursor_.execute('INSERT INTO client (skype_id, manufacturer, logged_in_user) VALUES (%s, %s, %s)',
                            (get_skype_id, manufacture, sk_token_id,))
                mysql.connection.commit()
                # return redirect(url_for('classify-contacts', sk_user=session['skype_id']))

            cursor = mysql.connection.cursor()
            cursor.execute('SELECT DISTINCT skype_id FROM client WHERE logged_in_user=%s', (sk_token_id,))
            data1 = list(cursor.fetchall())
            data1 = ",".join([x[0] for x in data1])
            client_ids = data1.split(",")
            # mysql.connection.commit()

            cursor.execute('SELECT DISTINCT skype_id FROM vendor WHERE logged_in_user=%s', (sk_token_id,))
            data2 = list(cursor.fetchall())
            data2 = ",".join([x[0] for x in data2])
            vendor_ids = data2.split(",")
            # mysql.connection.commit()

            vendor_client_ids = list(set(vendor_ids) | set(client_ids))

            cursor.execute('SELECT skype_id FROM contact_info WHERE logged_in_user=%s', (sk_token_id,))
            data3 = list(cursor.fetchall())
            data3 = ",".join([x[0] for x in data3])
            contact_ids = data3.split(",")
            # mysql.connection.commit()

            final_ids = list(set(contact_ids) - set(vendor_client_ids))
            # print(final_ids)

            return render_template('classify-contacts.html', sk_user=session['skype_id'], final_ids=final_ids)
        else:
            return redirect(url_for('dashboard'))

    except Exception as e:
        print(str(e))


@app.route('/details', methods=['GET', 'POST'])
def details():
    try:
        if not session.get('ivisions_user'):
            return redirect(url_for('login'))

        if request.method == 'POST':
            deal_type = request.form.get('deal_type')
            tb_row = request.form.get('tb_row')
            rowList = tb_row.split('-:::-')

        return render_template('details.html', rowList=rowList, deal_type=deal_type, sk_user=session['skype_id'])

    except Exception as e:
        print("Exception : ", str(e))

@app.route('/broadcast', methods=['GET', 'POST'])
def broadcast():
    try:
        if not session.get('ivisions_user'):
            return redirect(url_for('login'))

        if request.method == 'POST':
            country = request.form.get('country_selected').lower()
            supplier = request.form.get('supplier_selected').lower()
            manufacture = request.form.get('manufact_selected')
            p_type = request.form.get('type_selected')
            message = request.form.get('detail_tArea')
            sk = Skype(tokenFile=".tokens_File")
            logged_id = str(sk).split('UserId:')[1].strip()

            print(country, supplier, manufacture, p_type, message)

            if session['skype_id']:
                sk_id = session['skype_id']
                sk_pwd = session['skype_pwd']
                sk = Skype(sk_id, sk_pwd)

            cursor = mysql.connection.cursor()
            if country == "all":
                cursor.execute('SELECT skype_id FROM contact_info WHERE logged_in_user=%s', (logged_id,))
                data = list(cursor.fetchall())
                data = ",".join([x[0] for x in data])
                all_ids = data.split(',')
                mysql.connection.commit()
                filtered_ids = []

                cursor1 = mysql.connection.cursor()
                if supplier == 'client':
                    if manufacture and p_type:
                        cursor1.execute('SELECT DISTINCT skype_id FROM client WHERE manufacturer=%s AND type=%s AND logged_in_user=%s',
                                        (manufacture, p_type, logged_id,))
                    elif manufacture:
                        cursor1.execute('SELECT DISTINCT skype_id FROM client WHERE manufacturer=%s AND logged_in_user=%s',
                                        (manufacture, logged_id,))
                    data1 = list(cursor1.fetchall())
                    data1 = ",".join([x[0] for x in data1])
                    filtered_ids = data1.split(",")
                    mysql.connection.commit()

                elif supplier == 'vendor':
                    if manufacture and p_type:
                        cursor1.execute('SELECT DISTINCT skype_id FROM vendor WHERE manufacturer=%s AND type=%s AND logged_in_user=%s',
                                        (manufacture, p_type, logged_id,))
                    elif manufacture:
                        cursor1.execute('SELECT DISTINCT skype_id FROM vendor WHERE manufacturer=%s AND logged_in_user=%s',
                                        (manufacture, logged_id,))
                    data1 = list(cursor1.fetchall())
                    data1 = ",".join([x[0] for x in data1])
                    filtered_ids = data1.split(",")
                    mysql.connection.commit()

                elif supplier == 'vendorclient':
                    if manufacture and p_type:
                        cursor1.execute('SELECT skype_id FROM vendor WHERE manufacturer=%s AND type=%s AND logged_in_user=%s UNION SELECT skype_id FROM client WHERE manufacturer=%s AND type=%s AND logged_in_user=%s',
                                        (manufacture, p_type, logged_id, manufacture, p_type, logged_id,))
                    elif manufacture:
                        cursor1.execute('SELECT skype_id FROM vendor WHERE manufacturer=%s AND logged_in_user=%s UNION SELECT skype_id FROM client WHERE manufacturer=%s AND logged_in_user=%s',
                                        (manufacture, logged_id, manufacture, logged_id,))
                    data1 = list(cursor1.fetchall())
                    data1 = ",".join([x[0] for x in data1])
                    filtered_ids = data1.split(",")
                    mysql.connection.commit()

                # print(filtered_ids)
                try:
                    for chat_id in filtered_ids:
                        if not "8:" in chat_id:
                            chat_id = "8:" + chat_id

                        ch = sk.chats[chat_id]
                        ch.sendMsg(message)
                except:
                    pass

            else:
                cursor.execute('SELECT skype_id FROM contact_info WHERE country=%s AND logged_in_user=%s', (country, logged_id))
                data = list(cursor.fetchall())
                data = ",".join([x[0] for x in data])
                all_ids = data.split(',')
                # print(all_ids)
                mysql.connection.commit()
                filtered_ids = []
                final_ids = []
                cursor1 = mysql.connection.cursor()
                if supplier == 'client':
                    if manufacture and p_type:
                        cursor1.execute('SELECT DISTINCT skype_id FROM client WHERE manufacturer=%s AND type=%s AND logged_in_user=%s',
                                        (manufacture, p_type, logged_id))
                    elif manufacture:
                        cursor1.execute('SELECT DISTINCT skype_id FROM client WHERE manufacturer=%s AND logged_in_user=%s',
                                        (manufacture, logged_id))

                    data1 = list(cursor1.fetchall())
                    data1 = ",".join([x[0] for x in data1])
                    filtered_ids = data1.split(",")
                    # print(filtered_ids)
                    final_ids = list(set(all_ids) & set(filtered_ids))
                    # print(final_ids)
                    mysql.connection.commit()

                if supplier == 'vendor':
                    if manufacture and p_type:
                        cursor1.execute('SELECT DISTINCT skype_id FROM vendor WHERE manufacturer=%s AND type=%s AND logged_in_user=%s',
                                        (manufacture, p_type, logged_id))
                    elif manufacture:
                        cursor1.execute('SELECT DISTINCT skype_id FROM vendor WHERE manufacturer=%s AND logged_in_user=%s',
                                        (manufacture, logged_id))

                    data1 = list(cursor1.fetchall())
                    data1 = ",".join([x[0] for x in data1])
                    filtered_ids = data1.split(",")
                    # print(filtered_ids)
                    final_ids = list(set(all_ids) & set(filtered_ids))
                    # print(final_ids)
                    mysql.connection.commit()

                if supplier == 'vendorclient':
                    if manufacture and p_type:
                        cursor1.execute('SELECT skype_id FROM vendor WHERE manufacturer=%s AND type=%s AND logged_in_user=%s UNION SELECT skype_id FROM client WHERE manufacturer=%s AND type=%s AND logged_in_user=%s',
                                        (manufacture, p_type, logged_id, manufacture, p_type, logged_id))
                    elif manufacture:
                        cursor1.execute('SELECT skype_id FROM vendor WHERE manufacturer=%s AND logged_in_user=%s UNION SELECT skype_id FROM client WHERE manufacturer=%s AND logged_in_user=%s',
                                        (manufacture, logged_id, manufacture, logged_id))

                    data1 = list(cursor1.fetchall())
                    data1 = ",".join([x[0] for x in data1])
                    filtered_ids = data1.split(",")
                    # print(filtered_ids)
                    final_ids = list(set(all_ids) & set(filtered_ids))
                    # print(final_ids)
                    mysql.connection.commit()

                # print(final_ids)
                try:
                    for chat_id in filtered_ids:
                        if not "8:" in chat_id:
                            chat_id = "8:" + chat_id

                        ch = sk.chats[chat_id]
                        ch.sendMsg(message)
                except:
                    pass

        return render_template('broadcast.html', sk_user=session['skype_id'], countries=countries_dict)

    except Exception as e:
        print(str(e))

@app.route('/client',methods=['GET', 'POST'])
def client():
    try:
        if not session.get('ivisions_user'):
            return redirect(url_for('login'))

        get_read_client_file = ""
        dir_files = os.listdir(app.config['UPLOAD_PATH'])
        sk = Skype(tokenFile=".tokens_File")
        logged_id = str(sk).split('UserId:')[1].strip()
        for dir in dir_files:
            file_check = 'final_clients_' + logged_id
            if file_check in dir:
                get_read_client_file = app.config['UPLOAD_PATH'] + dir

        if get_read_client_file != "":
            from datetime import date, timedelta
            today_ = date.today()
            final_client_df = pd.read_csv(get_read_client_file)
            client_cursor = mysql.connection.cursor()
            client_cursor.execute('SELECT skype_id FROM client WHERE logged_in_user=%s', (logged_id,))
            first_check_client = client_cursor.fetchone()
            if not first_check_client:
                sql_insert_client = "INSERT INTO client (skype_id, conv_date, conversation, manufacturer, logged_in_user) VALUES (%s, %s, %s, %s, %s)"
                client_cursor.executemany(sql_insert_client, list(zip(final_client_df['Person'],
                                                               final_client_df['date'],
                                                               final_client_df['conversation_client'],
                                                               final_client_df['manufacturer'],
                                                               final_client_df['session_user'])))
                mysql.connection.commit()
            else:
                today_dataframe_client = final_client_df.loc[final_client_df['date'] == str(today_)]
                if today_dataframe_client.shape[0] > 0:
                    sql_count_stmt = 'SELECT COUNT(*) FROM client WHERE conv_date = %s AND logged_in_user=%s'
                    client_cursor.execute(sql_count_stmt, (today_, logged_id,))
                    db_rows_count = client_cursor.fetchone()[0]
                    if today_dataframe_client.shape[0] > db_rows_count:
                        sql_check_date = 'DELETE FROM client WHERE conv_date = %s AND logged_in_user=%s'
                        client_cursor.execute(sql_check_date, (today_, logged_id,))
                        mysql.connection.commit()
                        sql_update_client = "INSERT INTO client (skype_id, conv_date, conversation, manufacturer, logged_in_user) VALUES (%s, %s, %s, %s, %s)"
                        client_cursor.executemany(sql_update_client, list(zip(final_client_df['Person'],
                                                                       final_client_df['date'],
                                                                       final_client_df['conversation_client'],
                                                                       final_client_df['manufacturer'],
                                                                       final_client_df['session_user'])))
                        mysql.connection.commit()

        selected_val = request.form.get('manufact')
        selected_time = request.form.get('get_time')
        if selected_time == "-- Please choose --":
            selected_time = 90

        detail_id = request.form.get('detail_id')
        detail_date = request.form.get('detail_date')
        detail_conv = request.form.get('detail_conv')
        detail_manufact = request.form.get('detail_manufact')
        detail_tArea = request.form.get('detail_tArea')

        if detail_id and detail_date and detail_conv and detail_manufact and detail_tArea:
            if session['skype_id']:
                sk_id = session['skype_id']
                sk_pwd = session['skype_pwd']
                sk = Skype(sk_id, sk_pwd)

                chat_id = ""
                if not "8:" in detail_id:
                    chat_id = "8:" + detail_id
                else:
                    chat_id = detail_id

                ch = sk.chats[chat_id]
                ch.sendMsg(detail_tArea)

                cursor1 = mysql.connection.cursor()
                cursor1.execute('SELECT outgoing_chat FROM client WHERE skype_id=%s AND conv_date=%s AND conversation=%s AND manufacturer=%s AND logged_in_user=%s', (detail_id, detail_date, detail_conv, detail_manufact, logged_id,))
                chats = ""
                for item in cursor1.fetchall():
                    chats = chats + item[0]

                chats = chats + '-:::-' + detail_tArea
                print(detail_id, detail_date, detail_conv, detail_manufact, detail_tArea)
                cursor = mysql.connection.cursor()
                cursor.execute('UPDATE client SET outgoing_chat=%s WHERE skype_id=%s AND conv_date=%s AND conversation=%s AND manufacturer=%s AND logged_in_user=%s',(chats, detail_id, detail_date, detail_conv, detail_manufact, logged_id,))
                mysql.connection.commit()
            else:
                return redirect(url_for('ai'))

        if selected_val == None and detail_manufact != None:
            selected_val = detail_manufact

        if selected_val and selected_time:

            import datetime
            start_date = datetime.datetime.now() - datetime.timedelta(int(selected_time)-1)
            from_date = str(start_date).split(" ")[0]
            print(from_date)

            cursor = mysql.connection.cursor()
            cursor.execute('SELECT skype_id,conv_date,conversation,manufacturer FROM client WHERE manufacturer = %s AND conv_date >= %s AND logged_in_user=%s ORDER BY conv_date DESC', (selected_val, from_date, logged_id,))
            data = cursor.fetchall()
            mysql.connection.commit()

            return render_template('client.html', selected_val=selected_val, data=data, sk_user=session['skype_id'])
        else:
            return render_template('client.html', selected_val=selected_val, sk_user=session['skype_id'])

    except Exception as e:
        print(str(e))

@app.route('/vendor',methods=['GET', 'POST'])
def vendor():
    try:
        if not session.get('ivisions_user'):
            return redirect(url_for('login'))

        get_read_vendor_file = ""
        dir_files = os.listdir(app.config['UPLOAD_PATH'])
        sk = Skype(tokenFile=".tokens_File")
        logged_id = str(sk).split('UserId:')[1].strip()
        for dir in dir_files:
            file_check = 'final_vendors_' + logged_id
            if file_check in dir:
                get_read_vendor_file = app.config['UPLOAD_PATH'] + dir

        if get_read_vendor_file != "":
            from datetime import date, timedelta
            today_ = date.today()
            final_vendor_df = pd.read_csv(get_read_vendor_file)
            vendor_cursor = mysql.connection.cursor()
            vendor_cursor.execute('SELECT skype_id FROM vendor WHERE logged_in_user=%s', (logged_id,))
            first_check_client = vendor_cursor.fetchone()
            if not first_check_client:
                sql_insert_vendor = "INSERT INTO vendor (skype_id, conv_date, conversation, manufacturer, logged_in_user) VALUES (%s, %s, %s, %s, %s)"
                vendor_cursor.executemany(sql_insert_vendor, list(zip(final_vendor_df['Person'],
                                                                      final_vendor_df['date'],
                                                                      final_vendor_df['conversation_vendor'],
                                                                      final_vendor_df['manufacturer'],
                                                                      final_vendor_df['session_user'])))
                mysql.connection.commit()
            else:
                today_dataframe_vendor = final_vendor_df.loc[final_vendor_df['date'] == str(today_)]
                if today_dataframe_vendor.shape[0] > 0:
                    sql_count_stmt = 'SELECT COUNT(*) FROM vendor WHERE conv_date = %s AND logged_in_user=%s'
                    vendor_cursor.execute(sql_count_stmt, (today_, logged_id,))
                    db_rows_count = vendor_cursor.fetchone()[0]
                    if today_dataframe_vendor.shape[0] > db_rows_count:
                        sql_check_date = 'DELETE FROM vendor WHERE conv_date = %s AND logged_in_user=%s'
                        vendor_cursor.execute(sql_check_date, (today_, logged_id,))
                        mysql.connection.commit()
                        sql_update_vendor = "INSERT INTO vendor (skype_id, conv_date, conversation, manufacturer, logged_in_user) VALUES (%s, %s, %s, %s, %s)"
                        vendor_cursor.executemany(sql_update_vendor, list(zip(final_vendor_df['Person'],
                                                                              final_vendor_df['date'],
                                                                              final_vendor_df['conversation_vendor'],
                                                                              final_vendor_df['manufacturer'],
                                                                              final_vendor_df['session_user'])))
                        mysql.connection.commit()

        selected_val = request.form.get('manufact')
        selected_time = request.form.get('get_time')
        if selected_time == "-- Please choose --":
            selected_time = 90

        detail_id = request.form.get('detail_id')
        detail_date = request.form.get('detail_date')
        detail_conv = request.form.get('detail_conv')
        detail_manufact = request.form.get('detail_manufact')
        detail_tArea = request.form.get('detail_tArea')

        if detail_id and detail_date and detail_conv and detail_manufact and detail_tArea:
            if session['skype_id']:
                sk_id = session['skype_id']
                sk_pwd = session['skype_pwd']
                sk = Skype(sk_id, sk_pwd)
                chat_id = ""
                if not "8:" in detail_id:
                    chat_id = "8:" + detail_id
                else:
                    chat_id = detail_id
                ch = sk.chats[chat_id]
                ch.sendMsg(detail_tArea)
                cursor1 = mysql.connection.cursor()
                cursor1.execute('SELECT outgoing_chat FROM vendor WHERE skype_id=%s AND conv_date=%s AND conversation=%s AND manufacturer=%s AND logged_in_user=%s', (detail_id, detail_date, detail_conv, detail_manufact, logged_id,))
                chats = ""
                for item in cursor1.fetchall():
                    chats = chats + item[0]
                chats = chats + '-:::-' + detail_tArea
                print(detail_id, detail_date, detail_conv, detail_manufact, detail_tArea)
                cursor = mysql.connection.cursor()
                cursor.execute('UPDATE vendor SET outgoing_chat=%s WHERE skype_id=%s AND conv_date=%s AND conversation=%s AND manufacturer=%s AND logged_in_user=%s',(chats, detail_id, detail_date, detail_conv, detail_manufact, logged_id,))
                mysql.connection.commit()
            else:
                return redirect(url_for('ai'))

        if selected_val == None and detail_manufact != None:
            selected_val = detail_manufact

        if selected_val and selected_time:

            import datetime
            start_date = datetime.datetime.now() - datetime.timedelta(int(selected_time)-1)
            from_date = str(start_date).split(" ")[0]
            print(from_date)

            cursor = mysql.connection.cursor()
            cursor.execute('SELECT skype_id,conv_date,conversation,manufacturer FROM vendor WHERE manufacturer = %s AND conv_date >= %s AND logged_in_user=%s ORDER BY conv_date DESC', (selected_val, from_date, logged_id,))
            data = cursor.fetchall()
            mysql.connection.commit()

            return render_template('vendor.html', selected_val=selected_val, data=data, sk_user=session['skype_id'])
        else:
            return render_template('vendor.html', selected_val=selected_val, sk_user=session['skype_id'])

    except Exception as e:
        print(str(e))

def read_conversation(filename):
    try:
        final_dict = {}
        if filename != '':
            # print(filename, " this is in read conversation function")
            full_path = 'uploads/' + filename
            with open(full_path) as f:
                user_id_chat = ""
                if 'user_id_chat' in session:
                    user_id_chat = session['user_id_chat']

                # print(user_id_chat)
                data = json.load(f)
                export_date = data['exportDate'].split("T")[0]
                for person in data['conversations']:
                    contact = person['id']
                    status = person['properties']['conversationstatus']
                    if status != "AcceptPendingRecipient":
                        try:
                            if "@thread.skype" in contact:
                                conversations = person['MessageList']
                                if len(conversations) > 0:
                                    members = person['threadProperties']['members']
                                    members = members.replace("[", "")
                                    members = members.replace("]", "")
                                    members = members.replace('"', '')
                                    member_list = members.split(",")
                                    if len(member_list) > 1:
                                        for member in member_list:
                                            dict_dconv = {}
                                            date_conv = {}
                                            username = ""
                                            for conversation in conversations:
                                                if (conversation['from'] != user_id_chat) and (conversation['from'] == member) and (conversation['content']) and (conversation['messagetype'] == "RichText"):
                                                    cleantext = re.sub(re.compile('<.*?>'), '', conversation['content'])
                                                    extracted_date = conversation['originalarrivaltime'].split("T")[0]
                                                    if extracted_date in date_conv:
                                                        date_conv[extracted_date] += [html.unescape(cleantext)]
                                                    else:
                                                        date_conv[extracted_date] = [html.unescape(cleantext)]
                                                    username = member

                                            date_conv = dict(sorted(date_conv.items(), reverse=True))
                                            if date_conv:
                                                date_conv = dict(sorted(date_conv.items(), reverse=True))

                                                if username in dict_dconv:
                                                    dict_dconv[username].update(date_conv)
                                                else:
                                                    dict_dconv[username] = date_conv

                                            if dict_dconv:
                                                if contact in final_dict:
                                                    final_dict[contact].update(dict_dconv)
                                                else:
                                                    final_dict[contact] = dict_dconv

                            else:
                                conversations = person['MessageList']
                                if len(conversations) > 0:
                                    dict_dconv = {}
                                    date_conv = {}
                                    username = ""
                                    for conversation in conversations:
                                        if (conversation['from'] != user_id_chat) and (conversation['from'] == contact) and (conversation['content']):
                                            cleantext = re.sub(re.compile('<.*?>'), '', conversation['content'])
                                            extracted_date = conversation['originalarrivaltime'].split("T")[0]
                                            if extracted_date in date_conv:
                                                date_conv[extracted_date] += [html.unescape(cleantext)]
                                            else:
                                                date_conv[extracted_date] = [html.unescape(cleantext)]
                                            username = contact

                                    date_conv = dict(sorted(date_conv.items(), reverse=True))

                                    if date_conv:
                                        if username in final_dict:
                                            dict_dconv[username].update(date_conv)
                                        else:
                                            dict_dconv[username] = date_conv
                                    if dict_dconv:
                                        final_dict[contact] = dict_dconv
                        except Exception as e:
                            print(contact, str(e))

            # print(len(final_dict))
            sk = Skype(tokenFile=".tokens_File")
            sk_id = str(sk).split('UserId:')[1].strip()

            dataframe = pd.DataFrame(final_dict.items(), columns=['Person', 'Conversation'])
            # filename1 = "uploads/conversations_" + session['skype_id'].split('@')[0] + '_' + export_date + ".csv"
            filename1 = "uploads/conversations_" + sk_id + '_' + export_date + ".csv"
            dataframe.to_csv(filename1, index=False)
            classification()

    except Exception as e:
        print(str(e))

def update_contacts(contacts_file):
    try:
        get_read_conv_file = ""
        dir_files = os.listdir(app.config['UPLOAD_PATH'])
        print("this is update_contacts function ........... ")
        sk = Skype(tokenFile=".tokens_File")
        sk_id = str(sk).split('UserId:')[1].strip()
        for dir in dir_files:
            # file_check = 'conversations_' + session['skype_id'].split('@')[0]
            file_check = 'conversations_' + sk_id
            if file_check in dir:
                get_read_conv_file = app.config['UPLOAD_PATH'] + dir
        # print(get_read_conv_file)
        # print(contacts_file)
        get_file = get_read_conv_file.rsplit(".", 1)[0]
        get_file = get_file.split("/")[-1]
        get_file = get_file.split("_")[-1]
        last_export_date = get_file
        export_date = last_export_date
        # print(last_export_date)
        from datetime import date, timedelta
        today = date.today()
        dates_pd = pd.date_range(last_export_date, today - timedelta(days=0), freq='d')
        dates_list = []
        for date in dates_pd:
            date = str(date).strip()
            dates_list.append(date.split(" ")[0])
        dates_list.reverse()
        max_itr = 0
        if (len(dates_list) > 20):
            max_itr = len(dates_list)
        else:
            max_itr = 10
        new_contacts = []
        contacts_df = pd.read_csv(app.config['UPLOAD_PATH'] + contacts_file)
        contacts_df["creation_time"] = contacts_df["creation_time"].str.split(" ", n=1, expand=True)[0]
        df1 = contacts_df[(contacts_df['creation_time'] > export_date) & (contacts_df['type'] == 'Skype')]
        for index, row in df1.iterrows():
            username = '8:' + row['id']
            if username:
                new_contacts.append(username)
        print(new_contacts)
        if len(new_contacts) > 0:
            sk_id = session['skype_id']
            sk_pwd = session['skype_pwd']
            sk = Skype(sk_id, sk_pwd)
            full_conversation1 = {}
            for contact in new_contacts:
                try:
                    dict_dconv = {}
                    new_dict = {}
                    username = ""
                    flag = True
                    while flag:
                        n_chats = sk.chats[contact].getMsgs()
                        if n_chats:
                            for chat in n_chats:
                                sk_chat = str(chat).split("]")[1]
                                d1 = sk_chat.split("ClientId:")[0].split("Time:")[1].strip()
                                new_date = d1.split(" ")[0]
                                user_id = '8:' + sk_chat.split("ChatId:")[0].split("UserId:")[1].strip()
                                username = contact
                                if (new_date >= export_date) and (user_id == contact):
                                    content = sk_chat.split("Content:")[1].strip()
                                    cleantext = re.sub(re.compile('<.*?>'), '', content)
                                    if new_date in new_dict:
                                        new_dict[new_date] += [cleantext]
                                    else:
                                        new_dict[new_date] = [cleantext]
                                else:
                                    flag = False
                                    break
                        else:
                            break
                    if new_dict:
                        dict_dconv[username] = new_dict

                    if dict_dconv:
                        full_conversation1[contact] = dict_dconv

                except Exception as e:
                    print(contact, str(e))

            print(len(full_conversation1))
            dataframe1 = pd.read_csv(get_read_conv_file)
            dataframe2 = pd.DataFrame(full_conversation1.items(), columns=['Person', 'Conversation'])
            final_df = pd.concat([dataframe1, dataframe2], ignore_index=True)
            os.remove(get_read_conv_file)

            # print(sk_id)
            # filename2 = "uploads/conversations_" + session['skype_id'].split('@')[0]  + "_" + export_date + ".csv"
            filename2 = "uploads/conversations_" + sk_id + "_" + export_date + ".csv"
            final_df.to_csv(filename2, index=False)
            print("update contacts is done ....")
            classification()

        else:
            return redirect(url_for('dashboard'))

    except Exception as e:
        print(str(e))

def update_conversation():
    try:
        print("update conversation function is starts ...")
        get_read_conv_file = ""
        dir_files = os.listdir(app.config['UPLOAD_PATH'])

        sk = Skype(tokenFile=".tokens_File")
        sk_id = str(sk).split('UserId:')[1].strip()

        for dir in dir_files:
            # file_check = 'conversations_' + session['skype_id'].split('@')[0]
            file_check = 'conversations_' + sk_id
            if file_check in dir:
                print("conv : ", dir)
                get_read_conv_file = app.config['UPLOAD_PATH'] + dir
        # print(get_read_conv_file)
        import re
        from ast import literal_eval
        dataframe = pd.read_csv(get_read_conv_file)
        final_dict = {}
        for index, row in dataframe.iterrows():
            final_dict[row['Person']] = row['Conversation']
        print(len(final_dict))
        full_conversations = {}
        idx = 0
        for key in final_dict:
            contact = key
            conversation = literal_eval(final_dict[key])
            # print(idx, ". ", contact)
            if "@thread.skype" in contact:
                for key1 in conversation:
                    update_merge_dict = {}
                    update_conv = conversation[key1]
                    latest_date = list(update_conv.keys())[0]
                    try:
                        new_dict = {}
                        flag = True
                        while flag:
                            n_chats = sk.chats[contact].getMsgs()
                            if n_chats:
                                for chat in n_chats:
                                    sk_chat = str(chat).split("]")[1]
                                    d1 = sk_chat.split("ClientId:")[0].split("Time:")[1].strip()
                                    new_date = d1.split(" ")[0]
                                    user_id = sk_chat.split("ChatId:")[0].split("UserId:")[1].strip()
                                    if (new_date >= latest_date) and (user_id in key1):
                                        content = sk_chat.split("Content:")[1].strip()
                                        cleantext = re.sub(re.compile('<.*?>'), '', content)
                                        if new_date in new_dict:
                                            new_dict[new_date] += [cleantext]
                                        else:
                                            new_dict[new_date] = [cleantext]
                                    else:
                                        flag = False
                                        break
                            else:
                                break
                        if new_dict:
                            merge_dict = {**update_conv, **new_dict}
                            merge_dict = dict(sorted(merge_dict.items(), reverse=True))
                        if merge_dict:
                            update_merge_dict[key1] = merge_dict
                    except Exception as e:
                        print(contact, str(e))
                    if update_merge_dict:
                        full_conversations[contact] = update_merge_dict
            else:
                for key1 in conversation:
                    update_conv = conversation[key1]
                    latest_date = list(update_conv.keys())[0]
                    try:
                        new_dict = {}
                        flag = True
                        while flag:
                            n_chats = sk.chats[contact].getMsgs()
                            if n_chats:
                                for chat in n_chats:
                                    sk_chat = str(chat).split("]")[1]
                                    d1 = sk_chat.split("ClientId:")[0].split("Time:")[1].strip()
                                    new_date = d1.split(" ")[0]
                                    user_id = '8:' + sk_chat.split("ChatId:")[0].split("UserId:")[1].strip()
                                    if (new_date >= latest_date) and (user_id == contact):
                                        content = sk_chat.split("Content:")[1].strip()
                                        cleantext = re.sub(re.compile('<.*?>'), '', content)
                                        if new_date in new_dict:
                                            new_dict[new_date] += [cleantext]
                                        else:
                                            new_dict[new_date] = [cleantext]
                                    else:
                                        flag = False
                                        break
                            else:
                                break
                        if new_dict:
                            merge_dict = {**update_conv, **new_dict}
                            merge_dict = dict(sorted(merge_dict.items(), reverse=True))
                        update_merge_dict = {}
                        if merge_dict:
                            update_merge_dict[key1] = merge_dict
                        if update_merge_dict:
                            full_conversations[contact] = update_merge_dict
                    except Exception as e:
                        print(contact, str(e))
            idx += 1

        print(len(full_conversations))
        dataframe1 = pd.DataFrame(full_conversations.items(), columns=['Person', 'Conversation'])
        os.remove(get_read_conv_file)
        from datetime import date, timedelta
        today1 = date.today()

        # filename1 = "uploads/'conversations_" + session['skype_id'].split('@')[0] + "_" + str(today1) + ".csv"
        filename1 = "uploads/conversations_" + sk_id + "_" + str(today1) + ".csv"
        dataframe1.to_csv(filename1, index=False)
        classification()
        print("update conversation function is done...")

    except Exception as e:
        print("Exception : ", str(e))

def classification():
    try:
        vendor_primary = ['wts', 'offer', 'sell', 'selling', 'available', 'distribute', 'supply', 'deliver', 'physical',
                          'we offer', 'we have following stocks', 'we sell', 'stock offer', 'stock list',
                          'we want to move', 'we provide', 'we distribute', 'special offer', 'special price',
                          'special deal', 'sell-out', 'we supply', 'we deliver', 'we have on stock', 'we have physical',
                          'willing to sell', 'goods in stock', 'promotional offer', 'for volume order',
                          'check out my offer', 'do you need', 'closing deals', 'i have a source', 'wir liefern',
                          'wir bieten an', 'unsere angebote', 'unsere lagerware', 'wir haben']
        client_primary = ['wtb', 'want to buy', 'looking for', 'need', 'like to purchase', 'do you have',
                          'we need urgently', 'please offer', 'i would like to request', 'we are requesting',
                          'if you have', 'willing to buy', 'send prices', 'send availability',
                          'what stocks do you have', 'send your stocks', 'send your list', 'requesting list', 'demand',
                          'we require', 'we want to order', 'anything new', 'do you got', 'any update', 'want', 'wish',
                          'search', 'anything good', 'anything special', 'keep me posted', 'can you get',
                          'can you supply', 'can you provide', 'can you arrange', 'can you manage', 'organize',
                          'wir suchen', 'wir brauchen', 'suche', 'brauche', 'kaufe', 'kaufen', 'anfrage', 'anfragen',
                          'gesuche', 'biete mir an', 'bitte ambieten', 'angebot', 'wir fragen an', 'besorgen',
                          'benotigen']

        final_apple = ['apple', 'macbook', 'mac', 'imac', 'pro display xdr', 'iphone', 'watch se', 'watch nike se',
                       'apple watch', 'ipad', 'ipod', 'airpod', 'earpod']
        final_samsung = ['samsung', 'galaxy', 'samsung note', 'omnia w', 'giorgio armani', 'packet neo', 'glamor',
                         'wave', 'ch @ t', 'fold', 'xcover 2', 'xcover 3', 'xcover 4', 'xcover 4s', 'xcover 550',
                         'xcover pro', 'z fold2', 'z flip']
        final_huawei = ['huawei', 'nova', 'nexus 6p']
        final_lg = ['lg', 'velvet', 'wing', 'google nexus', 'joy', 'optimus', 'alicia', 'leon', 'sapphire', 'x cam',
                    'cookie', 'x power', 'viewty', 'bello', 'etna', 'anna', 'spirit', 'x screen', 'jaguar', 'stylus']
        final_xiaomi = ['xioami', 'redmi', 'pocophonoe', 'black shark', 'ascend', 'nova', 'shotx']
        final_sony = ['sony', 'xperia']
        final_lenovo = ['lenovo']

        print("Classification function starts ...")
        from datetime import date, timedelta
        today_ = date.today()
        # print(today_)

        get_read_conv_file = ""
        dir_files = os.listdir(app.config['UPLOAD_PATH'])

        sk = Skype(tokenFile=".tokens_File")
        sk_id = str(sk).split('UserId:')[1].strip()
        for dir in dir_files:
            file_check = 'conversations_' + sk_id
            if file_check in dir:
                get_read_conv_file = app.config['UPLOAD_PATH'] + dir

        print(get_read_conv_file)
        dataframe = pd.read_csv(get_read_conv_file)
        conversations_new = []
        conversations_new.extend(dataframe['Conversation'].tolist())

        final_ = []
        result_ = []
        timings_ = []

        import ast
        for i in range(len(conversations_new)):
            result_ = ast.literal_eval(conversations_new[i])
            final_.append(list(result_.values()))
            timings_.append(list(result_.keys()))

        end_conversation = []
        end_keys = []
        for i in range(len(final_)):
            end_conversation.append(list(final_[i][0].values()))
            end_keys.append(list(final_[i][0].keys()))

        import re
        for i in range(len(end_conversation)):
            for j in range(len(end_conversation[i])):
                for k in range(len(end_conversation[i][j])):
                    s = re.sub('\s+', ' ', end_conversation[i][j][k])
                    clean = re.compile('<.*?>')
                    text = re.sub(clean, '', s)
                    end_conversation[i][j][k] = text.lower()

        # print(end_conversation[0])
        # print("kmeans starts ... ")
        #
        # from sklearn.feature_extraction.text import TfidfVectorizer
        # from sklearn.cluster import KMeans
        #
        # vectorizer = TfidfVectorizer(stop_words='english')
        # print(vectorizer)
        # X = vectorizer.fit_transform(end_conversation)
        # print(X)
        #
        # model = KMeans(n_clusters=3, init='k-means++', max_iter=100, n_init=1)
        # model.fit(X)
        #
        # order_centroids = model.cluster_centers_.argsort()[:, ::-1]
        # terms = vectorizer.get_feature_names()
        #
        # for i in range(3):
        #     print('Cluster % d:' % i)
        #     for ind in order_centroids[i, :10]:
        #         print(' %s ' % terms[ind])

        vendor_classification = [[] for i in range(len(end_conversation))]
        client_classification = [[] for i in range(len(end_conversation))]

        for i in range(len(end_conversation)):
            for j in range(len(end_conversation[i])):
                for k in range(len(end_conversation[i][j])):
                    vendor_classification[i].append(
                        [{timings_[i][0]: {end_keys[i][j]: end_conversation[i][j][k]}} for word in vendor_primary if
                         (word in end_conversation[i][j][k])])
                    client_classification[i].append(
                        [{timings_[i][0]: {end_keys[i][j]: end_conversation[i][j][k]}} for word in client_primary if
                         (word in end_conversation[i][j][k])])

        for i in range(len(vendor_classification)):
            vendor_classification[i] = [k for j in vendor_classification[i] for k in j]

        for i in range(len(client_classification)):
            client_classification[i] = [k for j in client_classification[i] for k in j]

        person_vendor = []
        date_vendor = []
        date_conv_vendor = []
        conversation_vendor = []

        person_client = []
        date_client = []
        date_conv_client = []
        conversation_client = []

        for i in range(len(vendor_classification)):
            for j in range(len(vendor_classification[i])):
                person_vendor.append(list(vendor_classification[i][j].keys()))
                date_conv_vendor.append(list(vendor_classification[i][j].values()))

        for i in range(len(date_conv_vendor)):
            conversation_vendor.append(list(date_conv_vendor[i][0].values()))
            date_vendor.append(list(date_conv_vendor[i][0].keys()))

        for i in range(len(client_classification)):
            for j in range(len(client_classification[i])):
                person_client.append(list(client_classification[i][j].keys()))
                date_conv_client.append(list(client_classification[i][j].values()))

        for i in range(len(date_conv_client)):
            conversation_client.append(list(date_conv_client[i][0].values()))
            date_client.append(list(date_conv_client[i][0].keys()))

        person_vendor = [j for i in person_vendor for j in i]
        date_vendor = [j for i in date_vendor for j in i]
        conversation_vendor = [j for i in conversation_vendor for j in i]

        person_client = [j for i in person_client for j in i]
        date_client = [j for i in date_client for j in i]
        conversation_client = [j for i in conversation_client for j in i]

        for i in range(len(person_vendor)):
            if '@at#' in person_vendor[i]:
                person_vendor[i] = person_vendor[i].rsplit('@at#', 1)[0]
            else:
                person_vendor[i] = person_vendor[i]

        for i in range(len(person_client)):
            if '@at#' in person_client[i]:
                person_client[i] = person_client[i].rsplit('@at#', 1)[0]
            else:
                person_client[i] = person_client[i]

        for i in range(len(person_vendor)):
            if '8:' in person_vendor[i]:
                person_vendor[i] = person_vendor[i].rsplit('8:', 1)[1]
            else:
                person_vendor[i] = person_vendor[i]

        for i in range(len(person_client)):
            if '8:' in person_client[i]:
                person_client[i] = person_client[i].rsplit('8:', 1)[1]
            else:
                person_client[i] = person_client[i]

        manufacturer_vendor = []
        manufacturer_client = []

        for i in range(len(conversation_vendor)):
            if re.compile('|'.join(final_apple), re.IGNORECASE).search(conversation_vendor[i]):
                manufacturer_vendor.append('Apple')
            elif re.compile('|'.join(final_samsung), re.IGNORECASE).search(conversation_vendor[i]):
                manufacturer_vendor.append('Samsung')
            elif re.compile('|'.join(final_huawei), re.IGNORECASE).search(conversation_vendor[i]):
                manufacturer_vendor.append('Huawei')
            elif re.compile('|'.join(final_lenovo), re.IGNORECASE).search(conversation_vendor[i]):
                manufacturer_vendor.append('Lenovo')
            elif re.compile('|'.join(final_lg), re.IGNORECASE).search(conversation_vendor[i]):
                manufacturer_vendor.append('LG')
            elif re.compile('|'.join(final_xiaomi), re.IGNORECASE).search(conversation_vendor[i]):
                manufacturer_vendor.append('Xiaomi')
            elif re.compile('|'.join(final_sony), re.IGNORECASE).search(conversation_vendor[i]):
                manufacturer_vendor.append('Sony')
            else:
                manufacturer_vendor.append('General')

        for i in range(len(conversation_client)):
            if re.compile('|'.join(final_apple), re.IGNORECASE).search(conversation_client[i]):
                manufacturer_client.append('Apple')
            elif re.compile('|'.join(final_samsung), re.IGNORECASE).search(conversation_client[i]):
                manufacturer_client.append('Samsung')
            elif re.compile('|'.join(final_huawei), re.IGNORECASE).search(conversation_client[i]):
                manufacturer_client.append('Huawei')
            elif re.compile('|'.join(final_lenovo), re.IGNORECASE).search(conversation_client[i]):
                manufacturer_client.append('Lenovo')
            elif re.compile('|'.join(final_lg), re.IGNORECASE).search(conversation_client[i]):
                manufacturer_client.append('LG')
            elif re.compile('|'.join(final_xiaomi), re.IGNORECASE).search(conversation_client[i]):
                manufacturer_client.append('Xiaomi')
            elif re.compile('|'.join(final_sony), re.IGNORECASE).search(conversation_client[i]):
                manufacturer_client.append('Sony')
            else:
                manufacturer_client.append('General')

        final_dataframe_vendor = pd.DataFrame()

        final_dataframe_vendor['Person'] = person_vendor
        final_dataframe_vendor['date'] = date_vendor
        final_dataframe_vendor['conversation_vendor'] = conversation_vendor
        final_dataframe_vendor['manufacturer'] = manufacturer_vendor
        final_dataframe_vendor.insert(4, 'session_user', sk_id)
        final_dataframe_vendor = final_dataframe_vendor[final_dataframe_vendor.astype(str)['manufacturer'] != 'General']
        final_dataframe_vendor = final_dataframe_vendor.drop_duplicates(
            subset=['Person', 'date', 'conversation_vendor'])

        final_dataframe_client = pd.DataFrame()

        final_dataframe_client['Person'] = person_client
        final_dataframe_client['date'] = date_client
        final_dataframe_client['conversation_client'] = conversation_client
        final_dataframe_client['manufacturer'] = manufacturer_client
        final_dataframe_client.insert(4, 'session_user', sk_id)
        final_dataframe_client = final_dataframe_client[final_dataframe_client.astype(str)['manufacturer'] != 'General']
        final_dataframe_client = final_dataframe_client.drop_duplicates(
            subset=['Person', 'date', 'conversation_client'])

        vendor_filename = "uploads/final_vendors_" + sk_id + ".csv"
        client_filename = "uploads/final_clients_" + sk_id + ".csv"

        if os.path.exists(vendor_filename):
            os.remove(vendor_filename)
        final_dataframe_vendor.to_csv(vendor_filename, index=False)

        if os.path.exists(client_filename):
            os.remove(client_filename)
        final_dataframe_client.to_csv(client_filename, index=False)

        print("Classification function ends ....")

    except Exception as e:
        print("Exception : ", str(e))