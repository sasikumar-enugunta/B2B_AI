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
from skpy import Skype
import json
import html
import pandas as pd
import re

# from update_conversation import update_conversation
# from classification import classification
from new_classification import classify

countries_dict = {"AF": "Afghanistan", "AL": "Albania", "DZ": "Algeria", "AX": "Aland Islands", "AS": "American Samoa", "AI": "Anguilla", "AD": "Andorra", "AO": "Angola", "AN": "Antilles - Netherlands ", "AG": "Antigua and Barbuda", "AQ": "Antarctica", "AR": "Argentina", "AM": "Armenia", "AU": "Australia", "AT": "Austria", "AW": "Aruba", "AZ": "Azerbaijan", "BA": "Bosnia and Herzegovina", "BB": "Barbados", "BD": "Bangladesh", "BE": "Belgium", "BF": "Burkina Faso", "BG": "Bulgaria", "BH": "Bahrain", "BI": "Burundi", "BJ": "Benin", "BM": "Bermuda", "BN": "Brunei Darussalam", "BO": "Bolivia", "BR": "Brazil", "BS": "Bahamas", "BT": "Bhutan", "BV": "Bouvet Island", "BW": "Botswana", "BV": "Belarus", "BZ": "Belize", "KH": "Cambodia", "CM": "Cameroon", "CA": "Canada", "CV": "Cape Verde", "CF": "Central African Republic", "TD": "Chad", "CL": "Chile", "CN": "China", "CX": "Christmas Island", "CC": "Cocos (Keeling) Islands", "CO": "Colombia", "CG": "Congo", "CI": "Cote D'Ivoire (Ivory Coast)", "CK": "Cook Islands", "CR": "Costa Rica", "HR": "Croatia (Hrvatska)", "CU": "Cuba", "CY": "Cyprus", "CZ": "Czech Republic", "CD": "Democratic Republic of the Congo", "DJ": "Djibouti", "DK": "Denmark", "DM": "Dominica", "DO": "Dominican Republic", "EC": "Ecuador", "EG": "Egypt", "SV": "El Salvador", "TP": "East Timor", "EE": "Estonia", "GQ": "Equatorial Guinea", "ER": "Eritrea", "ET": "Ethiopia", "FI": "Finland", "FJ": "Fiji", "FK": "Falkland Islands (Malvinas)", "FM": "Federated States of Micronesia", "FO": "Faroe Islands", "FR": "France", "FX": "France, Metropolitan", "GF": "French Guiana", "PF": "French Polynesia", "GA": "Gabon", "GM": "Gambia", "DE": "Germany", "GH": "Ghana", "GI": "Gibraltar", "GB": "Great Britain (UK)", "GD": "Grenada", "GE": "Georgia", "GR": "Greece", "GL": "Greenland", "GN": "Guinea", "GP": "Guadeloupe", "GS": "S. Georgia and S. Sandwich Islands", "GT": "Guatemala", "GU": "Guam", "GW": "Guinea-Bissau", "GY": "Guyana", "HK": "Hong Kong", "HM": "Heard Island and McDonald Islands", "HN": "Honduras", "HT": "Haiti", "HU": "Hungary", "ID": "Indonesia", "IE": "Ireland", "IL": "Israel", "IN": "India", "IO": "British Indian Ocean Territory", "IQ": "Iraq", "IR": "Iran", "IT": "Italy", "JM": "Jamaica", "JO": "Jordan", "JP": "Japan", "KE": "Kenya", "KG": "Kyrgyzstan", "KI": "Kiribati", "KM": "Comoros", "KN": "Saint Kitts and Nevis", "KP": "Korea (North)", "KR": "Korea (South)", "KW": "Kuwait", "KY": "Cayman Islands", "KZ": "Kazakhstan", "LA": "Laos", "LB": "Lebanon", "LC": "Saint Lucia", "LI": "Liechtenstein", "LK": "Sri Lanka", "LR": "Liberia", "LS": "Lesotho", "LT": "Lithuania", "LU": "Luxembourg", "LV": "Latvia", "LY": "Libya", "MK": "Macedonia", "MO": "Macao", "MG": "Madagascar", "MY": "Malaysia", "ML": "Mali", "MW": "Malawi", "MR": "Mauritania", "MH": "Marshall Islands", "MQ": "Martinique", "MU": "Mauritius", "YT": "Mayotte", "MT": "Malta", "MX": "Mexico", "MA": "Morocco", "MC": "Monaco", "MD": "Moldova", "MN": "Mongolia", "MM": "Myanmar", "MP": "Northern Mariana Islands", "MS": "Montserrat", "MV": "Maldives", "MZ": "Mozambique", "NA": "Namibia", "NC": "New Caledonia", "NE": "Niger", "NF": "Norfolk Island", "NG": "Nigeria", "NI": "Nicaragua", "NL": "Netherlands", "NO": "Norway", "NP": "Nepal", "NR": "Nauru", "NU": "Niue", "NZ": "New Zealand (Aotearoa)", "OM": "Oman", "PA": "Panama", "PE": "Peru", "PG": "Papua New Guinea", "PH": "Philippines", "PK": "Pakistan", "PL": "Poland", "PM": "Saint Pierre and Miquelon", "CS": "Serbia and Montenegro", "PN": "Pitcairn", "PR": "Puerto Rico", "PS": "Palestinian Territory", "PT": "Portugal", "PW": "Palau", "PY": "Paraguay", "QA": "Qatar", "RE": "Reunion", "RO": "Romania", "RU": "Russian Federation", "RW": "Rwanda", "SA": "Saudi Arabia", "WS": "Samoa", "SH": "Saint Helena", "VC": "Saint Vincent and the Grenadines", "SM": "San Marino", "ST": "Sao Tome and Principe", "SN": "Senegal", "SC": "Seychelles", "SL": "Sierra Leone", "SG": "Singapore", "SK": "Slovakia", "SI": "Slovenia", "SB": "Solomon Islands", "SO": "Somalia", "ZA": "South Africa", "ES": "Spain", "SD": "Sudan", "SR": "Suriname", "SJ": "Svalbard and Jan Mayen", "SE": "Sweden", "CH": "Switzerland", "SY": "Syria", "SU": "USSR (former)", "SZ": "Swaziland", "TW": "Taiwan", "TZ": "Tanzania", "TJ": "Tajikistan", "TH": "Thailand", "TL": "Timor-Leste", "TG": "Togo", "TK": "Tokelau", "TO": "Tonga", "TT": "Trinidad and Tobago", "TN": "Tunisia", "TR": "Turkey", "TM": "Turkmenistan", "TC": "Turks and Caicos Islands", "TV": "Tuvalu", "UA": "Ukraine", "UG": "Uganda", "AE": "United Arab Emirates", "UK": "United Kingdom", "US": "United States", "UM": "United States Minor Outlying Islands", "UY": "Uruguay", "UZ": "Uzbekistan", "VU": "Vanuatu", "VA": "Vatican City State", "VE": "Venezuela", "VG": "Virgin Islands (British)", "VI": "Virgin Islands (U.S.)", "VN": "Viet Nam", "WF": "Wallis and Futuna", "EH": "Western Sahara", "YE": "Yemen", "YU": "Yugoslavia (former)", "ZM": "Zambia", "ZR": "Zaire (former)", "ZW": "Zimbabwe"}

app = Flask(__name__)

app.secret_key = 'secret'

app.config['MYSQL_HOST'] = 'mysql3000.mochahost.com'
app.config['MYSQL_USER'] = 'ivision1_ivision'
app.config['MYSQL_PASSWORD'] = 'iVision'
app.config['MYSQL_DB'] = 'ivision1_ivisions_b2bai'

# app.config['MYSQL_HOST'] = 'Pia.mysql.eu.pythonanywhere-services.com'
# app.config['MYSQL_USER'] = 'Pia'
# app.config['MYSQL_PASSWORD'] = 'Forever_2'
# app.config['MYSQL_DB'] = 'ivisions_b2bai'

mysql = MySQL(app)
app.config['UPLOAD_PATH'] = 'uploads/'

first_time = True

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
            sk = Skype(tokenFile=session['token_file'])
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
            sk = Skype(tokenFile=session['token_file'])
            logged_id = str(sk).split('UserId:')[1].strip()
            print(logged_id)
            cursor = mysql.connection.cursor()
            sql_query = ""
            if request.form.get('supplier_selected'):
                selected_supplier = request.form.get('supplier_selected')
                if selected_supplier == 'client':
                    sql_query = 'SELECT DISTINCT(c.skype_id), ci.display_name, c.manufacturer' \
                                ' FROM client c INNER JOIN contact_info ci' \
                                ' ON c.skype_id = ci.skype_id' \
                                ' WHERE c.type = "" AND c.logged_in_user = %s'
                elif selected_supplier == 'vendor':
                    sql_query = 'SELECT DISTINCT(v.skype_id), ci.display_name, v.manufacturer' \
                                ' FROM vendor v INNER JOIN contact_info ci' \
                                ' ON v.skype_id = ci.skype_id' \
                                ' WHERE v.type = "" AND v.logged_in_user = %s'

            cursor.execute(sql_query, (logged_id,))
            data = cursor.fetchall()
            mysql.connection.commit()

            return render_template('group.html', sk_user=session['skype_id'], data=data, supplier_=selected_supplier)
        else:
            return render_template('group.html', sk_user=session['skype_id'])

    except Exception as e:
        print(str(e))

@app.route('/dashboard')
def dashboard():
    try:
        if not session.get('ivisions_user'):
            return redirect(url_for('login'))

        if session.get('skype_id'):
            global first_time
            if first_time:
                first_time = False
                return redirect(url_for('upload'))
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
                    token_filename = ".tokens_File_" + session['ivisions_user']
                    session['token_file'] = token_filename
                    sk = Skype(email_id, pwd, token_filename)
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
                            cursor1.execute('INSERT INTO ai_login (login_user, password, skype_id) VALUES (%s, %s, %s) ', (email_id, pwd, user_id,))
                            mysql.connection.commit()

                            cursor2 = mysql.connection.cursor()
                            cursor2.execute('INSERT INTO tasks (skype_id) VALUES (%s)', (user_id,))
                            mysql.connection.commit()

                            return redirect(url_for('upload_json'))
                        # elif not account['last_updated_conv']:
                        #     return redirect(url_for('upload_json'))
                        # elif not account['last_updated_contacts']:
                        #     return redirect(url_for('upload'))
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
                sk = Skype(tokenFile=session['token_file'])
                sk_id = str(sk).split('UserId:')[1].strip()
                uploaded_file = request.files['selectFiles1']
                filename = secure_filename(uploaded_file.filename)
                filename_ = filename.split('.')[0]
                filename_ += '_' + sk_id + '.csv'
                if filename != '':
                    # file_ext = os.path.splitext(filename_)[1]
                    uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename_))
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('SELECT * FROM ai_login WHERE login_user = % s AND password = % s', (session['skype_id'], session['skype_pwd'],))
                    account = cursor.fetchone()
                    if not account['csv_file']:
                        cursor1 = mysql.connection.cursor()
                        cursor1.execute('UPDATE ai_login SET csv_file=%s WHERE login_user=%s AND password=%s ', (filename_, session['skype_id'], session['skype_pwd'],))
                        mysql.connection.commit()

                    data_csv = pd.DataFrame()
                    data_contacts = pd.DataFrame()
                    data_csv = pd.read_csv(os.path.join(app.config['UPLOAD_PATH'], filename_))
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
                        sql_delete = "DELETE * FROM contact_info WHERE added_date=%s"
                        sql_delete.execute(sql_delete, (last_imported_date))
                        mysql.connection.commit()
                        new_contacts_df = data_contacts.loc[data_contacts['added_date'] >= last_imported_date]
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
                            update_contacts(filename, sk, sk_id)             # from outer python file
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
            sk = Skype(tokenFile=session['token_file'])
            sk_id = str(sk).split('UserId:')[1].strip()
            # print(sk_id)

            file = request.files['file']
            filename = secure_filename(file.filename)

            file_ext = os.path.splitext(filename)[1]
            new_filename = filename.split('.')[0]
            new_filename += '_' + sk_id
            new_filename += file_ext
            # print(new_filename)

            save_path = os.path.join(app.config['UPLOAD_PATH'], new_filename)

            current_chunk = int(request.form['dzchunkindex'])

            try:
                with open(save_path, 'ab') as f:
                    f.seek(int(request.form['dzchunkbyteoffset']))
                    f.write(file.stream.read())

            except OSError:
                print('Could not write to file')

            total_chunks = int(request.form['dztotalchunkcount'])
            # print(current_chunk, ' ---- ', total_chunks)
            if current_chunk + 1 == total_chunks:
                if os.path.getsize(save_path) != int(request.form['dztotalfilesize']):
                    return redirect(url_for('upload_json'))
                else:
                    with open(save_path) as f:
                        data = json.load(f)
                        export_date = data['exportDate'].split("T")[0]

                    cursor = mysql.connection.cursor()
                    cursor.execute(
                        'UPDATE ai_login SET last_updated_conv=%s, json_file=%s, uploaded_json=%s WHERE login_user=%s AND password=%s ',
                        (export_date, new_filename, export_date, session['skype_id'], session['skype_pwd'],))
                    mysql.connection.commit()
                    read_conversation(new_filename)
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
            sk = Skype(tokenFile=session['token_file'])
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

            sk_token = Skype(tokenFile=session['token_file'])
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

            final_ids = list(set(contact_ids) - set(vendor_client_ids))

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
            sk = Skype(tokenFile=session['token_file'])
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

                # print("all : ", filtered_ids)
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

                # print("region : ", final_ids)
                try:
                    for chat_id in final_ids:
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
        sk = Skype(tokenFile=session['token_file'])
        logged_id = str(sk).split('UserId:')[1].strip()
        for dir in dir_files:
            file_check = 'final_clients_' + logged_id
            if file_check in dir:
                get_read_client_file = app.config['UPLOAD_PATH'] + dir

        print(get_read_client_file)
        if get_read_client_file != "":
            from datetime import date, timedelta
            today_ = date.today()
            final_client_df = pd.read_csv(get_read_client_file, engine='python')
            print(final_client_df.shape[0])
            client_cursor = mysql.connection.cursor()
            client_cursor.execute('SELECT skype_id FROM client WHERE logged_in_user=%s', (logged_id,))
            first_check_client = client_cursor.fetchone()
            # print(first_check_client)
            if not first_check_client:
                sql_insert_client = "INSERT INTO client (skype_id, conv_date, conversation, manufacturer, logged_in_user) VALUES (%s, %s, %s, %s, %s)"
                # print(sql_insert_client)
                client_cursor.executemany(sql_insert_client, list(zip(final_client_df['Skype_ID'],
                                                               final_client_df['Date'],
                                                               final_client_df['Conversation'],
                                                               final_client_df['Manufacturer'],
                                                               final_client_df['Session_user'])))
                mysql.connection.commit()
            else:
                today_dataframe_client = final_client_df.loc[final_client_df['Date'] == str(today_)]
                if today_dataframe_client.shape[0] > 0:
                    sql_count_stmt = 'SELECT COUNT(*) FROM client WHERE conv_date = %s AND logged_in_user=%s'
                    client_cursor.execute(sql_count_stmt, (today_, logged_id,))
                    db_rows_count = client_cursor.fetchone()[0]
                    if today_dataframe_client.shape[0] > db_rows_count:
                        sql_check_date = 'DELETE FROM client WHERE conv_date = %s AND logged_in_user=%s'
                        client_cursor.execute(sql_check_date, (today_, logged_id,))
                        mysql.connection.commit()
                        sql_update_client = "INSERT INTO client (skype_id, conv_date, conversation, manufacturer, logged_in_user) VALUES (%s, %s, %s, %s, %s)"
                        client_cursor.executemany(sql_update_client, list(zip(final_client_df['Skype_ID'],
                                                                       final_client_df['Date'],
                                                                       final_client_df['Conversation'],
                                                                       final_client_df['Manufacturer'],
                                                                       final_client_df['Session_user'])))
                        mysql.connection.commit()

            if os.path.exists(get_read_client_file):
                os.remove(get_read_client_file)

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
            # print(from_date)

            # cursor = mysql.connection.cursor()
            # cursor.execute('SELECT skype_id,conv_date,conversation,manufacturer FROM client WHERE manufacturer = %s AND conv_date >= %s AND logged_in_user=%s ORDER BY conv_date DESC', (selected_val, from_date, logged_id,))
            # data = cursor.fetchall()
            # print(type(data))
            # print(data)
            # mysql.connection.commit()

            cursor = mysql.connection.cursor()
            cursor.execute('SELECT skype_id,conv_date,conversation,manufacturer FROM client WHERE manufacturer = %s AND conv_date >= %s AND logged_in_user=%s ORDER BY conv_date DESC', (selected_val, from_date, logged_id,))
            data = [list(item) for item in cursor.fetchall()]
            # print(data)

            # get_read_conv_file = ""
            # for dir in dir_files:
            #     file_check = 'conversations_' + logged_id
            #     if file_check in dir:
            #         get_read_conv_file = app.config['UPLOAD_PATH'] + dir
            #
            # print(get_read_conv_file)
            #
            # data1 = pd.read_csv(get_read_conv_file)
            # final_dict = {}
            # for index, row in data1.iterrows():
            #     final_dict[row['Person']] = row['Conversation']
            # print(len(final_dict))
            #
            # for row in data:
            #     db_skype_id = row[0]
            #     db_skype_date = row[1]
            #     db_skype_conversation = row[2]
            #
            #     # print(db_skype_id, db_skype_date)
            #     # print(row[2])
            #
            #     from ast import literal_eval
            #     for key in final_dict:
            #         conversation = literal_eval(final_dict[key])
            #         for key1 in conversation:
            #             temp_db_id = '8:' + db_skype_id
            #             if key1 == temp_db_id:
            #                 update_conv = conversation[key1]
            #                 for key2 in update_conv:
            #                     if str(key2) == str(db_skype_date):
            #                         all_convs = update_conv[key2]
            #                         # print(all_convs)
            #                         for each_conv in all_convs:
            #                             filtered_sentence = each_conv.lower()
            #                             filtered_sentence = re.sub(r'\(.*\)', '', filtered_sentence)
            #                             filtered_sentence = re.sub(r'[^\w\s:/]', r'', filtered_sentence)
            #                             filtered_sentence = re.sub('\s+', ' ', filtered_sentence)
            #                             # print(filtered_sentence)
            #
            #                             if filtered_sentence == db_skype_conversation:
            #                                 # print(each_conv)
            #                                 row[2] = each_conv

                # temp_str1 = "this is new line character"
                # row[2] = temp_str1
                # print(row)

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
        sk = Skype(tokenFile=session['token_file'])
        logged_id = str(sk).split('UserId:')[1].strip()
        for dir in dir_files:
            file_check = 'final_vendors_' + logged_id
            if file_check in dir:
                get_read_vendor_file = app.config['UPLOAD_PATH'] + dir

        print(get_read_vendor_file)

        if get_read_vendor_file != "":
            from datetime import date, timedelta
            today_ = date.today()
            print(today_)
            final_vendor_df = pd.read_csv(get_read_vendor_file, engine='python')
            print(final_vendor_df.shape[0])
            vendor_cursor = mysql.connection.cursor()
            vendor_cursor.execute('SELECT skype_id FROM vendor WHERE logged_in_user=%s', (logged_id,))
            first_check_client = vendor_cursor.fetchone()
            # print(first_check_client)
            if not first_check_client:
                sql_insert_vendor = "INSERT INTO vendor (skype_id, conv_date, conversation, manufacturer, logged_in_user) VALUES (%s, %s, %s, %s, %s)"
                # print(sql_insert_vendor)
                vendor_cursor.executemany(sql_insert_vendor, list(zip(final_vendor_df['Skype_ID'],
                                                                      final_vendor_df['Date'],
                                                                      final_vendor_df['Conversation'],
                                                                      final_vendor_df['Manufacturer'],
                                                                      final_vendor_df['Session_user'])))
                mysql.connection.commit()
            else:
                today_dataframe_vendor = final_vendor_df.loc[final_vendor_df['Date'] == str(today_)]
                if today_dataframe_vendor.shape[0] > 0:
                    sql_count_stmt = 'SELECT COUNT(*) FROM vendor WHERE conv_date = %s AND logged_in_user=%s'
                    vendor_cursor.execute(sql_count_stmt, (today_, logged_id,))
                    db_rows_count = vendor_cursor.fetchone()[0]
                    if today_dataframe_vendor.shape[0] > db_rows_count:
                        sql_check_date = 'DELETE FROM vendor WHERE conv_date = %s AND logged_in_user=%s'
                        vendor_cursor.execute(sql_check_date, (today_, logged_id,))
                        mysql.connection.commit()
                        sql_update_vendor = "INSERT INTO vendor (skype_id, conv_date, conversation, manufacturer, logged_in_user) VALUES (%s, %s, %s, %s, %s)"
                        vendor_cursor.executemany(sql_update_vendor, list(zip(final_vendor_df['Skype_ID'],
                                                                              final_vendor_df['Date'],
                                                                              final_vendor_df['Conversation'],
                                                                              final_vendor_df['Manufacturer'],
                                                                              final_vendor_df['Session_user'])))
                        mysql.connection.commit()

            if os.path.exists(get_read_vendor_file):
                os.remove(get_read_vendor_file)

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
        conv_contacts = []
        if filename != '':
            # print(filename, " this is in read conversation function")
            full_path = app.config['UPLOAD_PATH'] + filename
            with open(full_path) as f:
                user_id_chat = ""
                if 'user_id_chat' in session:
                    user_id_chat = session['user_id_chat']

                print(user_id_chat)
                data = json.load(f)

                export_date = data['exportDate'].split("T")[0]
                print(export_date)

                for person in data['conversations']:
                    contact = person['id']
                    status = person['properties']['conversationstatus']
                    if status != "AcceptPendingRecipient":
                        try:
                            if "@thread.skype" in contact:
                                conversations = person['MessageList']
                                if len(conversations) > 0:
                                    conv_contacts.append(contact)
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
                                    conv_contacts.append(contact)
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
            sk = Skype(tokenFile=session['token_file'])
            sk_id = str(sk).split('UserId:')[1].strip()
            # print(sk_id)

            print(full_path)
            if os.path.exists(full_path):
                os.remove(full_path)

            dataframe = pd.DataFrame(final_dict.items(), columns=['Person', 'Conversation'])
            filename_ = "conversations_" + sk_id + '_' + export_date + ".csv"
            filename1 = app.config['UPLOAD_PATH'] + filename_
            dataframe.to_csv(filename1, index=False)

            # print(filename_)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT filename FROM tasks WHERE skype_id = %s', (sk_id,))
            get_file = cursor.fetchone()
            # print(get_file)
            if not get_file['filename']:
                cursor1 = mysql.connection.cursor()
                cursor1.execute('UPDATE tasks SET filename=%s WHERE skype_id=%s',(filename_, sk_id,))
                mysql.connection.commit()
            classify(sk_id, filename_)

    except Exception as e:
        print(str(e))

def get_file_update_contacts(filename=False):
    get_read_conv_file = ""
    dir_files = os.listdir(app.config['UPLOAD_PATH'])
    print("this is update_contacts function ........... ")
    sk = Skype(tokenFile=session['token_file'])
    sk_id = str(sk).split('UserId:')[1].strip()
    for dir in dir_files:
        file_check = 'conversations_' + sk_id
        if file_check in dir:
            get_read_conv_file = app.config['UPLOAD_PATH'] + dir
    if filename:
        return get_read_conv_file, sk, app.config['UPLOAD_PATH'] + filename, session['skype_id'], session['skype_pwd']
    else:
        return None

if __name__ == '__main__':
    app.run()
