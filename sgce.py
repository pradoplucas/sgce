import requests
import os
import time

url = 'http://apl.utfpr.edu.br/extensao/certificados/listaPublica'

url_search = 'http://apl.utfpr.edu.br/extensao/certificados/listaCertificadosPublicos'

nome = 'Lucas do Prado Pinto'

data_search = {'hdnPesquisa': 'pesquisa', 'cmbPesquisa': 'D', 'txtPesquisa': ''}

data_search['txtPesquisa'] = nome

events_2014 = []
events_2015 = []
events_2016 = []
events_2017 = []
events_2018 = []
events_2019 = []
events_2020 = []

certificates_2014 = []
certificates_2015 = []
certificates_2016 = []
certificates_2017 = []
certificates_2018 = []
certificates_2019 = []
certificates_2020 = []

def main():
    get_id()
    get_certificate()
    preparation_download()

##Encontra e separa o id de cada evento no campus CP
def get_id():
    global events_2014, events_2015, events_2016, events_2017, events_2018, events_2019, events_2020

    print('IDs: Init')

    events = []
    years = ['2014', '2015', '2016', '2017', '2018', '2019', '2020']
    data = {'txtCampus':'13', 'txtAno':''}

    for year in years:
        data['txtAno'] = year

        res = requests.post(url, data = data)
        
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

    print('IDs: Done')

def get_certificate():
    global certificates_2014, certificates_2015, certificates_2016, certificates_2017, certificates_2018, certificates_2019, certificates_2020

    cookie = requests.post(url_search, data = data_search).cookies

    print('\nYears: Init')
    certificates_2014 = events(events_2014, cookie)
    print('2014: Done')
    certificates_2015 = events(events_2015, cookie)
    print('2015: Done')
    certificates_2016 = events(events_2016, cookie)
    print('2016: Done')
    certificates_2017 = events(events_2017, cookie)
    print('2017: Done')
    certificates_2018 = events(events_2018, cookie)
    print('2018: Done')
    certificates_2019 = events(events_2019, cookie)
    print('2019: Done')
    certificates_2020 = events(events_2020, cookie)
    print('2020: Done')
    print('Years: Done')

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
    global certificates_2014, certificates_2015, certificates_2016, certificates_2017, certificates_2018, certificates_2019, certificates_2020

    os.mkdir(nome)

    print('\nDownloads: Init')
    download(nome + '/2014/', certificates_2014)
    print('2014: Done')
    download(nome + '/2015/', certificates_2015)
    print('2015: Done')
    download(nome + '/2016/', certificates_2016)
    print('2016: Done')
    download(nome + '/2017/', certificates_2017)
    print('2017: Done')
    download(nome + '/2018/', certificates_2018)
    print('2018: Done')
    download(nome + '/2019/', certificates_2019)
    print('2019: Done')
    download(nome + '/2020/', certificates_2020)
    print('2020: Done')
    print('Downloads: Done')

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
