import requests
import argparse
import os
import time
import shutil

##Receive the datas by parameter and save in the variables
parser = argparse.ArgumentParser()
#Required
parser.add_argument('-n', action = 'store', dest = 'name', 
                    required = True, help = 'full name')
#Not required
parser.add_argument('-c', action = 'store', dest = 'campus', 
                    choices = [ 'CT', 'AP', 'CM', 'DV', 'FB', 'GP', 'LD', 
                                'MD', 'PB', 'PG', 'SH', 'TD', 'CP'], 
                    help = 'acronym - two letters', 
                    default = 'CP')
#Not required
parser.add_argument('-y', action = 'store', dest = 'year', 
                    choices = [ '2014', '2015', '2016', '2017', '2018', '2019', '2020'], 
                    help = 'especific year', 
                    default = 'All')

name = parser.parse_args().name
campus_id = parser.parse_args().campus
year_id = parser.parse_args().year

##Creates and initializes the necessary variables
#URLs nedded
url = 'http://apl.utfpr.edu.br/extensao/certificados/listaPublica'
url_search = 'http://apl.utfpr.edu.br/extensao/certificados/listaCertificadosPublicos'
#Data nedded to find the name
data_search = {'hdnPesquisa': 'pesquisa', 'cmbPesquisa': 'D', 'txtPesquisa': ''}
data_search['txtPesquisa'] = name
#Data nedded to find campus and set the IDs of the events
campus_all = {  'CT': '1', 'AP': '2', 'CM': '3', 'DV': '4', 'FB': '5', 
                'GP': '6', 'LD': '7', 'MD': '8', 'PB': '9', 'PG': '10', 
                'SH': '11', 'TD': '12', 'CP': '13'}
data_id = {'txtCampus':'', 'txtAno':''}
data_id['txtCampus'] = campus_all[campus_id]

##Initializes the arrays that will be used to save the IDS of the events and...
events = []
#...the codes of the certificates
certificates = []

##The main function
def main():
    print(f'\nName: {name}\nCampus: {campus_id}\nYear/s: {year_id}\n')

    get_id()
    get_certificate()
    preparation_download()

##Find and save the IDs of each event
def get_id():
    global events, data_id

    print('-IDs- -> Init')

    years = ['2014', '2015', '2016', '2017', '2018', '2019', '2020']

    if(year_id != 'All'):
        years = []
        years.append(year_id)

    for year in years:
        data_id['txtAno'] = year

        res = requests.post(url, data = data_id)
        res = res.text.split('value="">Selecione')[1].split('value="')
        res.pop(0)

        events_ = [year]

        for events_raw in res:
            events_.append(events_raw.split('" >')[0])

        events.append(events_)

    print('-IDs- -> Done\n')

def get_certificate():
    global certificates

    cookie = requests.post(url_search, data = data_search).cookies

    print('-Years- -> Init')

    for events_year in events:

        certificates.append(get_events(events_year, cookie))

        print(f'{certificates[len(certificates) - 1][0]} -> Done ({len(certificates[len(certificates) - 1])} certificate/s)')

    print('-Years- -> Done')

def get_events(events_, cookie):
    certificates_ = [events_[0]]

    events_.pop(0)

    data = {'txtEvento':''}

    for id in events_:
        data['txtEvento'] = id
        results = requests.post(url, data = data, cookies = cookie).text

        n_cert = results.count('http://apl.utfpr.edu.br/extensao/certificados/validar/')
    
        if(n_cert != 0):
            results = results.split('http://apl.utfpr.edu.br/extensao/certificados/validar/')

            results.pop(0)

            for result in results:
                certificates_.append(result.split('">')[0])

    return certificates_

def preparation_download():
    global certificates

    try:
        os.mkdir(name)
        print()
    except:
        print()

    print('-Downloads- -> Init')

    for certificates_year in certificates:
        download(certificates_year)

    print('-Downloads- -> Done\n')

def download(certificates_):
    url_base = 'http://apl.utfpr.edu.br/extensao/emitir/'

    if(len(certificates_) > 0):
        path = name + '/' + certificates_[0] + '/'

        try:
            os.mkdir(path)
        except:
            shutil.rmtree(path)
            os.mkdir(path)

        certificates_.pop(0)

        for id in certificates_:
            url_ = url_base + id

            r = requests.get(url_, allow_redirects=True)

            open(path + id + '.pdf', 'wb').write(r.content)

if __name__ == '__main__':
    main()
