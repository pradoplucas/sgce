import requests
import json
import os
import datetime

path_old = '101120-150038-13-14/'

def main():

    #   CT -> 1   AP -> 2    CM -> 3    DV -> 4    FB -> 5    GP -> 6   LD -> 7
    #   MD -> 8   PB -> 9    PG -> 10   SH -> 11   TD -> 12   CP -> 13
    campus = '13'

    #   2013 -> 2014 -> 2015 -> 2016 -> 2017 -> 2018 -> 2019 -> 2020
    year = '2015'

    url = 'http://apl.utfpr.edu.br/extensao/certificados/listaPublica/'
    url_search = 'http://apl.utfpr.edu.br/extensao/certificados/listaCertificadosPublicos/'

    events = []
    students = []

    events = stage_1(campus, year, url)
    students = stage_2(events, url_search)
    stage_3(events, students, campus)
    stage_id(events, url_search)

def stage_1(campus_, year_, url_):
    events_ = []

    data_ = {'txtCampus':campus_, 'txtAno':year_}

    results = requests.post(url_, data = data_).text
    results = results.split('value="">Selecione')[1].split('value="')
    results.pop(0)

    for events_raw in results:
        events_.append(events_raw.split('" >')[0])

    return events_

def stage_2(events_, url_):
    students_ = {}

    for id in events_:
        sub_id = 0
        text_raw = []
        
        while True:
            results = requests.post(url_ + str(sub_id), data = {'txtEvento': id}).text
            
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
                students_[aux_name].append(aux_cert)
            else:
                students_[aux_name] = [aux_cert]

    return students_

def stage_3(events_, students_, campus_):

    dt = datetime.datetime.now()
    date = str(dt.strftime("%d")) + str(dt.strftime("%m")) + str(dt.strftime("%y"))
    time = str(dt.strftime("%H")) + str(dt.strftime("%M")) + str(dt.strftime("%S"))
    path = ''

    if(campus_ == ''):
        campus_ = '0'

    path = date + '-' + time + '-' + campus_
    os.mkdir(path)

    open(path + '/result.json', 'wt').write(json.dumps(students_))
    open(path + '/events.json', 'wt').write(json.dumps(events_))

def stage_id(events_, url_):
    e_old = json.loads(open(path_old + 'events.json').read())
    s_old = json.loads(open(path_old + 'result.json').read())
    
    e_diff = []

    for e_new in events_:
        if(e_old.count(e_new) == 0):
            e_diff.append(e_new)

    s_diff = stage_2(e_diff, url_)

    for name_new, cert_new in s_diff.items():
        if name_new in s_old:
            for cert in cert_new:
                s_old[name_new].append(cert)
        else:
            s_old[name_new] = cert_new

    #open(path_old + 'e_diff_to_now.json', 'wt').write(json.dumps(e_diff))

    #open(path_old + 's_diff_to_now.json', 'wt').write(json.dumps(s_diff))

    open(path_old + 's_new.json', 'wt').write(json.dumps(s_old))

if __name__ == '__main__':
    main()
