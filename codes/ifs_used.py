    elif(action == 1):
        events = stage_1(campus, year, url)
        #events = stage_1(campus, year, url)
        #students = stage_2(events, url_search)
        #stage_3(events, students, year)

        evnt1 = {year[0]:[]}
        evnt2 = {year[0]:[]}

        i = 0

        tam_events = len(events[year[0]])

        for ev in events[year[0]]:
            if(i < int(tam_events/2)):
                evnt1[year[0]].append(ev)
            else:
                evnt2[year[0]].append(ev)

            i += 1

        '''
        #print(len(events[year[0]]))
        #print(events[year[0]])
        print('\n\n' + str(len(evnt1[year[0]])))
        print(evnt1[year[0]])
        print('\n\n' + str(len(evnt2[year[0]])))
        print(evnt2[year[0]])

        print(len(events[year[0]]))

        open('aaa.json', 'wt').write(json.dumps(events))


        students = stage_2(evnt1, url_search)
        stage_3(evnt1, students, year, '_1')
        '''
        students = stage_2(evnt2, url_search)
        stage_3(evnt2, students, year, '_2')    
    
    elif(action == 3):
        results_json = json.loads(open('results.json').read())

        nome1 = 'Lucas do Prado Pinto'
        nome2 = 'Lucas Do Prado Pinto'
        nome3 = 'lucas do prado pinto'
        nome4 = 'LUCAS DO PRADO PINTO'
        
        try:
            print(nome1 + '\n' + json.dumps(results_json[nome1]) + '\n')
        except:
            print(nome1 + ' -> Não')

        try:
            print(nome2 + '\n' + json.dumps(results_json[nome2]) + '\n')
        except:
            print(nome2 + ' -> Não')

        try:
            print(nome3 + '\n' + json.dumps(results_json[nome3]) + '\n')
        except:
            print(nome3 + ' -> Não')

        try:
            print(nome4 + '\n' + json.dumps(results_json[nome4]) + '\n')
        except:
            print(nome4 + ' -> Não')

    elif(action == 4):
        no_sensitive = {}

        sensitive = json.loads(open('results.json').read())

        for name, year_dict in sensitive.items():
            name_title = name.title()
            
            if name_title not in no_sensitive:
                no_sensitive[name_title] = year_dict
            
            else:
                for year, certName_list in year_dict.items():
                    if year not in no_sensitive[name_title]:
                        no_sensitive[name_title][year] = certName_list

                    else:
                        for certName in certName_list:
                            no_sensitive[name_title][year].append(certName)

        open('results_no.json', 'wt').write(json.dumps(no_sensitive))    

    elif(action == 5):
        name = 'MARIN\u00caS RIBEIRO DOS SANTOS'

        name_upper = name.upper()

        results_upper = json.loads(open('results_upper.json').read())

        #for year in results_no[name_title]:
        #    print(json.dumps(results_no[name_title][year]) + '\n')

        print(name_upper + '\n' + json.dumps(results_upper[name_upper]) + '\n')

    elif(action == 6):
        results_upper = {}

        results_title = json.loads(open('results_title.json').read())

        for name, values in results_title.items():
            results_upper[name.upper()] = values

        open('results_upper.json', 'wt').write(json.dumps(results_upper))  

    elif(action == 7):
        res_new = {}

        res = json.loads(open('output/results.json').read())

        for name, year_dict in res.items():
            name_new = name.rstrip()
            
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