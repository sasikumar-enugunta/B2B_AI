import os
# import pandas as pd

# import nltk
from nltk.tokenize import word_tokenize

# import app

def classify(sk_id, get_read_conv_file):

    try:
        vendor_primary = ['wts', 'offer', 'sell', 'selling',
                          'we offer', 'we have following stocks', 'we sell', 'want to sell', 'stock offer', 'stock list',
                          'we want to move', 'we provide', 'we distribute', 'special offer', 'special price',
                          'special deal', 'sell-out', 'we supply', 'we deliver', 'we have on stock', 'we have physical',
                          'willing to sell', 'goods in stock', 'promotional offer', 'for volume order',
                          'check out my offer', 'do you need', 'closing deals', 'i have a source', 'wir liefern',
                          'wir bieten an', 'unsere angebote', 'unsere lagerware', 'wir haben']

        client_primary = ['wtb', 'want to buy', 'looking for', 'i need', 'like to purchase', 'want to purchase', 'do you have',
                          'we need urgently', 'please offer', 'i would like to request', 'we are requesting',
                          'if you have', 'willing to buy', 'send prices', 'send availability',
                          'what stocks do you have', 'send your stocks', 'send your list', 'requesting list', 'demand',
                          'we require', 'we want to order', 'anything new', 'do you got', 'any update', 'i want', 'we want', 'i wish to have',
                          'we wish to have', 'search', 'keep me posted', 'can you get',
                          'can you supply', 'can you provide', 'can you arrange', 'can you manage', 'can you organize',
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

        negative_words = ["dont", "don't", "not", "mightn't", "mustn't", "shouldn't", "wouldn't"]

        print("New_Classification function starts ...")
        # from datetime import date
        # today_ = date.today()

        import pandas as pd
        import re
        from ast import literal_eval

        skype_contact_id = []
        skype_contact_date = []
        skype_contact_conv = []

        if get_read_conv_file and sk_id:
            data = pd.read_csv(get_read_conv_file)
            final_dict = {}
            for index, row in data.iterrows():
                final_dict[row['Person']] = row['Conversation']
            print(len(final_dict))

            full_conversations = {}
            for key in final_dict:
                contact = key
                conversation = literal_eval(final_dict[key])
                for key1 in conversation:
                    update_conv = conversation[key1]
                    # print(key1, update_conv)
                    for key2 in update_conv:
                        all_convs = update_conv[key2]
                        # if key2 >= get_last_updated_date:
                        for each_conv in all_convs:
                            filtered_sentence = each_conv.lower()
                            filtered_sentence = re.sub(r'\(.*\)', '', filtered_sentence)
                            filtered_sentence = re.sub(r'[^\w\s:/]', r'', filtered_sentence)
                            filtered_sentence = re.sub('\s+', ' ', filtered_sentence)

                            if filtered_sentence:
                                if '8:' in key1:
                                    key1 = key1.rsplit('8:', 1)[1]
                                skype_contact_id.append(key1)
                                skype_contact_date.append(key2)
                                skype_contact_conv.append(filtered_sentence)

            vendor_contact_id = []
            vendor_contact_date = []
            vendor_contact_conv = []
            vendor_manufacturer = []
            vendor_session = []

            client_contact_id = []
            client_contact_date = []
            client_contact_conv = []
            client_manufacturer = []
            client_session = []

            vendor_dataframe = pd.DataFrame()
            client_dataframe = pd.DataFrame()

            for i in range(len(skype_contact_conv)):
                conversation = skype_contact_conv[i].lower()
                flag = True

                for word in negative_words:
                    if word in conversation:
                        flag = False

                if flag:
                    manufacturer_ = ""
                    if re.compile('|'.join(final_apple), re.IGNORECASE).search(conversation):
                        manufacturer_ = 'Apple'
                    elif re.compile('|'.join(final_samsung), re.IGNORECASE).search(conversation):
                        manufacturer_ = 'Samsung'
                    elif re.compile('|'.join(final_huawei), re.IGNORECASE).search(conversation):
                        manufacturer_ = 'Huawei'
                    elif re.compile('|'.join(final_lenovo), re.IGNORECASE).search(conversation):
                        manufacturer_ = 'Lenovo'
                    elif re.compile('|'.join(final_lg), re.IGNORECASE).search(conversation):
                        manufacturer_ = 'LG'
                    elif re.compile('|'.join(final_xiaomi), re.IGNORECASE).search(conversation):
                        manufacturer_ = 'Xiaomi'
                    elif re.compile('|'.join(final_sony), re.IGNORECASE).search(conversation):
                        manufacturer_ = 'Sony'
                    else:
                        manufacturer_ = 'General'

                    word_tokens = word_tokenize(conversation)
                    filtered_words_vendor = [w for w in word_tokens if w in vendor_primary]

                    if len(filtered_words_vendor) > 0:
                        # filtered_sentence = " ".join(filtered_words)
                        vendor_contact_id.append(skype_contact_id[i])
                        vendor_contact_date.append(skype_contact_date[i])
                        vendor_contact_conv.append(conversation)
                        vendor_manufacturer.append(manufacturer_)
                        vendor_session.append(sk_id)

                    filtered_words_client = [w for w in word_tokens if w in client_primary]
                    if len(filtered_words_client) > 0:
                        # filtered_sentence = " ".join(filtered_words)
                        client_contact_id.append(skype_contact_id[i])
                        client_contact_date.append(skype_contact_date[i])
                        client_contact_conv.append(conversation)
                        client_manufacturer.append(manufacturer_)
                        client_session.append(sk_id)

            vendor_dataframe['Skype_ID'] = vendor_contact_id
            vendor_dataframe['Date'] = vendor_contact_date
            vendor_dataframe['Conversation'] = vendor_contact_conv
            vendor_dataframe['Manufacturer'] = vendor_manufacturer
            vendor_dataframe['Session_user'] = vendor_session

            final_vendor_df = vendor_dataframe[vendor_dataframe['Manufacturer'] != 'General']
            print(final_vendor_df.shape[0])

            client_dataframe['Skype_ID'] = client_contact_id
            client_dataframe['Date'] = client_contact_date
            client_dataframe['Conversation'] = client_contact_conv
            client_dataframe['Manufacturer'] = client_manufacturer
            client_dataframe['Session_user'] = client_session

            final_client_df = client_dataframe[client_dataframe['Manufacturer'] != 'General']
            print(final_client_df.shape[0])

            vendor_filename = "/home/Pia/mysite/uploads/final_vendors_" + sk_id + ".csv"
            client_filename = "/home/Pia/mysite/uploads/final_clients_" + sk_id + ".csv"

            if os.path.exists(vendor_filename):
                os.remove(vendor_filename)
            final_vendor_df.to_csv(vendor_filename, index=False)

            if os.path.exists(client_filename):
                os.remove(client_filename)
            final_client_df.to_csv(client_filename, index=False)

            print('New_Classification function is done... ')

    except Exception as e:
        print("Exception : ", str(e))