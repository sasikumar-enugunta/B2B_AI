import os
from skpy import Skype
import pandas as pd

import update_classification

import mysql.connector

connection = mysql.connector.connect(
  host="mysql3000.mochahost.com",
  user="ivision1_ivision",
  password="iVision",
  database="ivision1_ivisions_b2bai"
)


def update_conversation():
    try:

        print("This is classification function ... ")

        full_path = '/home/Pia/mysite/uploads/'

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM tasks")
        get_rows = cursor.fetchall()
        print(get_rows)

        for row in get_rows:
            sk_id = row['skype_id']
            get_read_conv_file = row['filename']

            cursor.execute("SELECT login_user, password FROM ai_login WHERE skype_id=%s", (sk_id, ))
            get_credentials = cursor.fetchone()
            print(sk_id, get_read_conv_file, get_credentials['login_user'], get_credentials['password'])

            if get_credentials['login_user'] and get_credentials['password']:

                skype_login = get_credentials['login_user']
                skype_password = get_credentials['password']
                sk = Skype(skype_login, skype_password)

                if sk:

                    import re
                    from ast import literal_eval

                    dataframe = pd.read_csv(full_path + get_read_conv_file)
                    final_dict = {}
                    for index, row in dataframe.iterrows():
                        final_dict[row['Person']] = row['Conversation']

                    print(len(final_dict))
                    full_conversations = {}

                    from datetime import date
                    today1 = date.today()

                    filename_ = "conversations_" + sk_id + "_" + str(today1) + ".csv"
                    filename1 = full_path + filename_

                    cursor.execute('SELECT last_updated_conv FROM ai_login WHERE skype_id=%s', (sk_id,))
                    get_last_imported_date = cursor.fetchone()
                    print(get_last_imported_date)
                    get_last_imported_date = get_last_imported_date['last_updated_conv'].strftime("%Y-%m-%d")
                    print(get_last_imported_date)

                    if filename_ != get_read_conv_file:
                        cursor1 = connection.cursor()
                        cursor1.execute('UPDATE tasks SET filename=%s WHERE skype_id=%s', (filename_, sk_id,))
                        connection.commit()
                        print('File replacement successful')

                    if get_last_imported_date != str(today1):
                        cursor2 = connection.cursor()
                        cursor2.execute('UPDATE ai_login SET last_updated_conv=%s WHERE skype_id=%s', (str(today1), sk_id,))
                        connection.commit()

                    for key in final_dict:
                        contact = key
                        conversation = literal_eval(final_dict[key])
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

                    print(len(full_conversations))
                    dataframe1 = pd.DataFrame(full_conversations.items(), columns=['Person', 'Conversation'])
                    if os.path.exists(full_path + get_read_conv_file):
                        os.remove(full_path + get_read_conv_file)

                    dataframe1.to_csv(filename1, index=False)

                    print("update conversation is done ...")
                    print(sk_id, filename1, get_last_imported_date)
                    update_classification.update_classify(sk_id, filename1, get_last_imported_date)


    except Exception as e:
        print("Exception : ", str(e))


if __name__ == '__main__':
    update_conversation()
