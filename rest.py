def get_id():

    res = requests.post(url, data = {'txtCampus':'13'}).text.split('value="">Selecione')[1].split('value="')

    res.pop(0)

    events = []

    for events_raw in res:
        events.append(events_raw.split('" >')[0])

    #print(events)
    #print(len(events))

    return events

def get_id_year():
    events = []
    years = ['2014', '2015', '2016', '2017', '2018', '2019', '2020']
    data = {'txtCampus':'13', 'txtAno':''}

    for year in years:
        data['txtAno'] = year

        res = requests.post(url, data = data)
        
        res = res.text.split('value="">Selecione')[1].split('value="')

        res.pop(0)

        for events_raw in res:
            events.append(year + "-" + events_raw.split('" >')[0])

    #print(events)
    #print(len(events))

    return events

def get_certificate(events):

    cookie = requests.post(url_search, data = data_search).cookies

    certificates = []

    data = {'txtEvento':''}

    for id in events:

        #print(id)

        data['txtEvento'] = id
        results = requests.post(url, data = data, cookies = cookie).text

        n_cert = results.count('http://apl.utfpr.edu.br/extensao/certificados/validar/')
    
        if(n_cert != 0):
            results = results.split('http://apl.utfpr.edu.br/extensao/certificados/validar/')

            results.pop(0)

            for result in results:
                certificates.append(result.split('">')[0])
    
    #print(certificates)

    return certificates

def get_certificate_year(events):
    cookie = requests.post(url_search, data = data_search).cookies

    certificates = []

    data = {'txtEvento':''}

    for y_id in events:

        #print(id)

        year = y_id.split('-')[0]
        id = y_id.split('-')[1]

        data['txtEvento'] = id
        results = requests.post(url, data = data, cookies = cookie).text

        n_cert = results.count('http://apl.utfpr.edu.br/extensao/certificados/validar/')
    
        if(n_cert != 0):
            results = results.split('http://apl.utfpr.edu.br/extensao/certificados/validar/')

            results.pop(0)

            for result in results:
                certificates.append(year + "-" + result.split('">')[0])
    
    print(certificates)

    return certificates
