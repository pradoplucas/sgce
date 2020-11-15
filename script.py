import requests
import json
import os
import datetime
import shutil
from collections import OrderedDict 

#2014   -> 00:00:56
#2015   -> 00:04:38
#2015   -> 00:45:36
#2017/1 -> 00:32:14
#2017/2 -> 00:36:55
#2017/3 -> 00:43:09
#2018/1 -> 00:24:40
#2018/2 -> 00:21:36
#2018/3 -> 00:26:30
#2018/4 -> 00:23:24
#2018/5 -> 00:32:21
#2019/1 -> 00:18:53
#2019/2 -> 00:18:23
#2019/3 -> 00:27:13
#2019/4 -> 00:19:46
#2019/5 -> 00:21:37
#2019/6 -> 00:34:55
#2020/1 -> 00:29:47

#som a cada ano
#nome dos eventos
#separar funções

def main():
    #0 -> Update
    #1 -> Run
    #2 -> Join Certificates

    action = 3

    #   CT -> 1   AP -> 2    CM -> 3    DV -> 4    FB -> 5    GP -> 6   LD -> 7
    #   MD -> 8   PB -> 9    PG -> 10   SH -> 11   TD -> 12   CP -> 13
    campus = ''

    #   2013 -> 2014 -> 2015 -> 2016 -> 2017 -> 2018 -> 2019 -> 2020
    year = ['2014', '2015', '2016', '2017', '2018', '2019', '2020']
    #year = ['2020']

    url = 'http://apl.utfpr.edu.br/extensao/certificados/listaPublica/'
    url_search = 'http://apl.utfpr.edu.br/extensao/certificados/listaCertificadosPublicos/'

    events = {}
    students = {}

    if(action == 0):  
        events = stage_1(campus, year, url)
        stage_update(events, url_search)

    elif(action == 1):
        events = stage_1(campus, year, url)
        students = stage_2(events, url_search)
        stage_3(events, students, year)

    elif(action == 2):
        n_1 = 'c1'
        n_2 = 'c2'

        res = join_certificates(json.loads(open(n_1 + '.json').read()), json.loads(open(n_2 + '.json').read()))

        open(n_1 + '-' + n_2 + '.json', 'wt').write(json.dumps(res))

    elif(action == 3):
        res = json.loads(open('output/new_new_new_new_new_results.json').read())

        #for name in res:
        #    for name_1 in res:
        #        if(name_1 != name):
        #            if(name_1.find(name) != -1):
        #                print(name_1 + ' -> ' + name)

        #soma = 0

        #for name, ye in res.items():
        #    for y in ye:
        #        soma += len(res[name][y])

        #print(soma)

        #for name, ye in res.items():
        #    num_aux = name.find('  ')
        #    if num_aux != -1:
        #        print(name)
        #        soma += 1

        #print(soma)
        
        print(len(res))

    elif(action == 7):
        res_new = {}

        res = json.loads(open('output/results.json').read())

        for name, year_dict in res.items():
            name_new = name.replace("  ", " ")
            
            if name_new not in res_new:
                res_new[name_new] = year_dict
            
            else:
                for year, certName_list in year_dict.items():
                    if year not in res_new[name_new]:
                        res_new[name_new][year] = certName_list

                    else:
                        for certName in certName_list:
                            res_new[name_new][year].append(certName)

        open('output/new_results.json', 'wt').write(json.dumps(res_new))


def stage_1(campus_, year_, url_):
    events_ = {}

    for y in year_:

        events_[y] = []

        data_ = {'txtCampus': campus_, 'txtAno': y}

        results = requests.post(url_, data = data_).text
        results = results.split('value="">Selecione')[1].split('value="')
        results.pop(0)

        for events_raw in results:
            aux_event = events_raw.split('" >')

            events_[y].append([aux_event[0],aux_event[1].split('</option>')[0]])

    return events_

def stage_2(events_, url_):
    students_ = {}

    for y, e_list in events_.items():
        print('Start -> ' + y)
        time_start = datetime.datetime.now()

        for evnt in e_list:

            sub_id = 0
            text_raw = []
            
            while True:
                results = requests.post(url_ + str(sub_id), data = {'txtEvento': evnt[0]}).text
                
                if('\')">' in results):
                    results = results.split('\')">')
                    results.pop(0)
                    text_raw.extend(results)
                else:
                    break

                sub_id += 15

            for aux in text_raw:
                aux_name = aux[aux.find('>') + 1:aux.find('</')]
                aux_name = aux_name.upper()
                aux_name = aux_name.rstrip('*.- \'"')
                aux_name = aux_name.lstrip('*.- \'"')
                
                for i in range(3):
                    aux_name = aux_name.replace("  ", " ")

                aux_cert = aux.split('http://apl.utfpr.edu.br/extensao/certificados/validar/')[1].split('">')[0]

                if aux_name in students_:
                    if y in students_[aux_name]:
                        students_[aux_name][y].append([aux_cert, evnt[1]])
                    else:
                        students_[aux_name][y] = [[aux_cert, evnt[1]]]

                else:
                    students_[aux_name] = {}
                    students_[aux_name][y] = [[aux_cert, evnt[1]]]

        print('End -> ' + str(datetime.datetime.now() - time_start))

    return students_

def stage_3(events_, students_, year_):

    path = 'output'

    try:
        os.mkdir(path)
    except:
        #shutil.rmtree(path)
        #os.mkdir(path)
        print('\a')

    #open(path + '/results.json', 'wt').write(json.dumps(students_))
    #open(path + '/events.json', 'wt').write(json.dumps(events_))

    open('results.json', 'wt').write(json.dumps(students_))
    open('events.json', 'wt').write(json.dumps(events_))

def diff_events(events_old, events_new):

    events_diff = {}

    for year, e_new in events_new.items():
        for evnt in e_new:
            if year not in events_old:
                events_old[year] = []

            if(events_old[year].count(evnt) == 0):
                if year in events_diff:
                    events_diff[year].append([evnt])
                else:
                    events_diff[year] = [evnt]

    return events_diff

def join_certificates(certificates_1, certificates_2):

    for name, year_dict in certificates_1.items():
        for year, cert_list in year_dict.items():
            for cert in cert_list:
                if name in certificates_2:
                    if year in certificates_2[name]:
                        certificates_2[name][year].append(cert)
                    else:
                        certificates_2[name][year] = [cert]
                else:
                    certificates_2[name] = {}
                    certificates_2[name][year] = [cert]

    return certificates_2

def stage_update(events_, url_):
    e_old = json.loads(open('output/events.json').read())
    s_old = json.loads(open('output/results.json').read())
    
    e_diff = diff_events(e_old, events_)

    s_diff = stage_2(e_diff, url_)

    s_new = join_certificates(s_diff, s_old)

    dt = datetime.datetime.now()
    date = str(dt.strftime("%d")) + str(dt.strftime("%m")) + str(dt.strftime("%y"))
    time = str(dt.strftime("%H")) + str(dt.strftime("%M")) + str(dt.strftime("%S"))
    path = ''

    path = 'output/' + date + '-' + time + '-'

    if(len(e_diff) == 0):
        print('Nothing Changes..')
    
    else:
        print('Events Changes..')
        open(path + 'e_diff_to_now.json', 'wt').write(json.dumps(e_diff))
        open(path + 'events.json', 'wt').write(json.dumps(events_))

        if(len(s_diff) == 0):
            print('Certificates Dont Changes..')

        else:
            print('Certificates Changes..')
            open(path + 's_diff_to_now.json', 'wt').write(json.dumps(s_diff))
            open(path + 'results.json', 'wt').write(json.dumps(s_new))
    
if __name__ == '__main__':
    main()
