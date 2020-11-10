import requests
import json
import os
import datetime
import shutil

def main():
    update = False

    #   CT -> 1   AP -> 2    CM -> 3    DV -> 4    FB -> 5    GP -> 6   LD -> 7
    #   MD -> 8   PB -> 9    PG -> 10   SH -> 11   TD -> 12   CP -> 13
    campus = ''

    #   2013 -> 2014 -> 2015 -> 2016 -> 2017 -> 2018 -> 2019 -> 2020
    year = ['2014', '2015', '2016', '2017', '2018', '2019', '2020']
    #year = ['2014', '2015']

    url = 'http://apl.utfpr.edu.br/extensao/certificados/listaPublica/'
    url_search = 'http://apl.utfpr.edu.br/extensao/certificados/listaCertificadosPublicos/'

    events = {}
    students = {}

    if update:  
        events = stage_1(campus, year, url)
        stage_id(events, url_search)

    else:
        events = stage_1(campus, year, url)
        students = stage_2(events, url_search)
        stage_3(events, students)

def stage_1(campus_, year_, url_):
    events_ = {}

    for y in year_:

        events_[y] = []

        data_ = {'txtCampus': campus_, 'txtAno': y}

        results = requests.post(url_, data = data_).text
        results = results.split('value="">Selecione')[1].split('value="')
        results.pop(0)

        for events_raw in results:
            events_[y].append(events_raw.split('" >')[0])

    return events_

def stage_2(events_, url_):
    students_ = {}

    for y, e_list in events_.items():

        for e in e_list:

            sub_id = 0
            text_raw = []
            
            while True:
                results = requests.post(url_ + str(sub_id), data = {'txtEvento': e}).text
                
                if('\')">' in results):
                    results = results.split('\')">')
                    results.pop(0)
                    text_raw.extend(results)
                else:
                    break

                sub_id += 15

            for aux in text_raw:
                aux_name = aux[aux.find('>') + 1:aux.find('</')]
                aux_cert = aux.split('http://apl.utfpr.edu.br/extensao/certificados/validar/')[1].split('">')[0]

                if aux_name in students_:
                    if y in students_[aux_name]:
                        students_[aux_name][y].append(aux_cert)
                    else:
                        students_[aux_name][y] = [aux_cert]

                else:
                    students_[aux_name] = {}
                    students_[aux_name][y] = [aux_cert]

    return students_

def stage_3(events_, students_):

    path = 'output'

    try:
        os.mkdir(path)
    except:
        shutil.rmtree(path)
        os.mkdir(path)

    open(path + '/result.json', 'wt').write(json.dumps(students_))
    open(path + '/events.json', 'wt').write(json.dumps(events_))

def stage_id(events_, url_):
    e_old = json.loads(open('output/events.json').read())
    s_old = json.loads(open('output/result.json').read())
    
    e_diff = {}

    for y, e_new in events_.items():
        for e in e_new:
            if y not in e_old:
                e_old[y] = []

            if(e_old[y].count(e) == 0):
                if y in e_diff:
                    e_diff[y].append(e)
                else:
                    e_diff[y] = [e]
            

    s_diff = stage_2(e_diff, url_)

    for name, y_dict in s_diff.items():
        for y, cert_list in y_dict.items():
            for cert in cert_list:
                if name in s_old:
                    if y in s_old[name]:
                        s_old[name][y].append(cert)
                    else:
                        s_old[name][y] = [cert]
                else:
                    s_old[name] = {}
                    s_old[name][y] = [cert]

    dt = datetime.datetime.now()
    date = str(dt.strftime("%d")) + str(dt.strftime("%m")) + str(dt.strftime("%y"))
    time = str(dt.strftime("%H")) + str(dt.strftime("%M")) + str(dt.strftime("%S"))
    path = ''

    path = 'output/' + date + '-' + time + '-'


    #open(path + 'e_diff_to_now.json', 'wt').write(json.dumps(e_diff))
    #open(path + 's_diff_to_now.json', 'wt').write(json.dumps(s_diff))

    open(path + 'result.json', 'wt').write(json.dumps(s_old))
    open(path + 'events.json', 'wt').write(json.dumps(events_))

if __name__ == '__main__':
    main()
