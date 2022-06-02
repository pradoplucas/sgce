import requests
import argparse
import os
import time

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
events_2014 = []
events_2015 = []
events_2016 = []
events_2017 = []
events_2018 = []
events_2019 = []
events_2020 = []
#...the codes of the certificates
certificates_2014 = []
certificates_2015 = []
certificates_2016 = []
certificates_2017 = []
certificates_2018 = []
certificates_2019 = []
certificates_2020 = []

##The main function
def main():
    print(f'\nName: {name}\nCampus: {campus_id}\nYear/s: {year_id}\n')

    get_id()
    get_certificate()
    preparation_download()

##Find and save the IDs of each event
def get_id():
    global events_2014, events_2015, events_2016, events_2017
    global events_2018, events_2019, events_2020, data_id

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

        for events_raw in res:
            if(year == '2019'):
                events_2019.append(events_raw.split('" >')[0])
            elif(year == '2017'):
                events_2017.append(events_raw.split('" >')[0])            
            elif(year == '2016'):
                events_2016.append(events_raw.split('" >')[0])            
            elif(year == '2018'):
                events_2018.append(events_raw.split('" >')[0])            
            elif(year == '2020'):
                events_2020.append(events_raw.split('" >')[0])            
            elif(year == '2015'):
                events_2015.append(events_raw.split('" >')[0])        
            elif(year == '2014'):
                events_2014.append(events_raw.split('" >')[0])  

    print('-IDs- -> Done\n')

def get_certificate():
    global certificates_2014, certificates_2015, certificates_2016
    global certificates_2017, certificates_2018, certificates_2019 
    global certificates_2020

    cookie = requests.post(url_search, data = data_search).cookies

    print('-Years- -> Init')

    certificates_2014 = events(events_2014, cookie)
    print(f'2014 -> Done ({len(certificates_2014)} certificate/s)')

    certificates_2015 = events(events_2015, cookie)
    print(f'2015 -> Done ({len(certificates_2015)} certificate/s)')

    certificates_2016 = events(events_2016, cookie)
    print(f'2016 -> Done ({len(certificates_2016)} certificate/s)')

    certificates_2017 = events(events_2017, cookie)
    print(f'2017 -> Done ({len(certificates_2017)} certificate/s)')

    certificates_2018 = events(events_2018, cookie)
    print(f'2018 -> Done ({len(certificates_2018)} certificate/s)')

    certificates_2019 = events(events_2019, cookie)
    print(f'2019 -> Done ({len(certificates_2019)} certificate/s)')

    certificates_2020 = events(events_2020, cookie)
    print(f'2020 -> Done ({len(certificates_2020)} certificate/s)')

    print('-Years- -> Done\n')

def events(events, cookie):
    certificates = []

    data = {'txtEvento':''}

    for id in events:
        data['txtEvento'] = id
        results = requests.post(url, data = data, cookies = cookie).text

        n_cert = results.count('http://apl.utfpr.edu.br/extensao/certificados/validar/')
    
        if(n_cert != 0):
            results = results.split('http://apl.utfpr.edu.br/extensao/certificados/validar/')

            results.pop(0)

            for result in results:
                certificates.append(result.split('">')[0])

    return certificates

def preparation_download():
    global certificates_2014, certificates_2015, certificates_2016
    global certificates_2017, certificates_2018, certificates_2019 
    global certificates_2020

    os.mkdir(name)

    print('-Downloads- -> Init')

    download(name + '/2014/', certificates_2014)
    print('2014 -> Done')

    download(name + '/2015/', certificates_2015)
    print('2015 -> Done')

    download(name + '/2016/', certificates_2016)
    print('2016 -> Done')

    download(name + '/2017/', certificates_2017)
    print('2017 -> Done')

    download(name + '/2018/', certificates_2018)
    print('2018 -> Done')

    download(name + '/2019/', certificates_2019)
    print('2019 -> Done')

    download(name + '/2020/', certificates_2020)
    print('2020 -> Done')

    print('-Downloads- -> Done\n')

def download(path, certificates):
    url_base = 'http://apl.utfpr.edu.br/extensao/emitir/'

    if(len(certificates) > 0):
        os.mkdir(path)

        for cert in certificates:
            url_ = url_base + cert

            r = requests.get(url_, allow_redirects=True)

            open(path + cert + '.pdf', 'wb').write(r.content)

if __name__ == '__main__':
    main()
