import os
# from skpy import Skype
import pandas as pd
import re

import update_classification

def update_contacts(get_read_conv_file, contacts_file, sk, sk_id):
    try:
        full_path = '/home/Pia/mysite/uploads/'

        if get_read_conv_file and sk and contacts_file:
            full_path_file = full_path + get_read_conv_file
            get_file = full_path_file.rsplit(".", 1)[0]
            get_file = get_file.split("/")[-1]
            get_file = get_file.split("_")[-1]
            last_export_date = get_file
            export_date = last_export_date
            from datetime import date, timedelta
            today = date.today()
            dates_pd = pd.date_range(last_export_date, today - timedelta(days=0), freq='d')
            dates_list = []
            for date_ in dates_pd:
                date_ = str(date_).strip()
                dates_list.append(date_.split(" ")[0])
            dates_list.reverse()
            # max_itr = 0
            # if (len(dates_list) > 20):
            #     max_itr = len(dates_list)
            # else:
            #     max_itr = 10
            new_contacts = []
            contacts_df = pd.read_csv(full_path + contacts_file)
            contacts_df["creation_time"] = contacts_df["creation_time"].str.split(" ", n=1, expand=True)[0]
            df1 = contacts_df[(contacts_df['creation_time'] > export_date) & (contacts_df['type'] == 'Skype')]
            for index, row in df1.iterrows():
                username = '8:' + row['id']
                if username:
                    new_contacts.append(username)
            print(new_contacts)
            if len(new_contacts) > 0:
                # sk = Skype(sk_id, sk_pwd)
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
                if os.path.exists(full_path_file):
                    os.remove(full_path_file)

                filename2 = full_path + "conversations_" + sk_id + "_" + export_date + ".csv"
                final_df.to_csv(filename2, index=False)
                update_classification.update_classify()
                print("update contacts is done ....")

    except Exception as e:
        print(str(e))
