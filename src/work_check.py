import requests
from bs4 import BeautifulSoup as BS
import codecs

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
           }

url = 'https://www.work.ua/ru/jobs-kyiv-python/'
resp = requests.get(url, headers=headers)
soup = BS(resp.content, 'html.parser')
domain = 'https://www.work.ua'
jobs = []
errors = []
if resp.status_code == 200:
    soup = BS(resp.content, 'html.parser')
    main_div = soup.find('div', id='pjax-job-list')
    if main_div:
        div_list = main_div.find_all('div', attrs={'class': 'job-link'})
        for div in div_list:
            # print(div, end='\n\n\n\n\n\n\n') # обрати внимание, на какие элементы разделяется div_list # CHECK
            title = div.find('h2')
            # print(title.a.string)  # CHECK
            href = title.find('a')
            # print(href, domain + href['href']) # CHECK
            content = div.p.text#.strip()
            # print(content, type(content))    # CHECK
            logo = 'Unknown'
            if div.img:
                # print(div.img)    # CHECK
                logo = div.img['alt']
                # print(logo)
            jobs.append({
                'title': title.a.string,
                'url': domain + href['href'],
                'description': content,
                'logo': logo
            })
            # print(title.a.string,domain+href['href'],sep='\n',end='\n\n\n') # CHECK
    else:
        errors.append({'url': url, 'cause': 'Div does not exist', 'status_code': resp.status_code,})
        pass
else:
    errors.append({'url': url, 'cause': 'Page does not response', 'status_code': resp.status_code})





def rabota_CHECK():
    jobs = []
    errors = []
    domain = 'https://rabota.ua'
    url = 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2'
    resp = requests.get(url=url, headers=headers)
    soup = BS(resp.content, 'html.parser')

    # CHECK find() -----------------------------------------------------------------------------------------------------
    print('soup = BS(resp.content, "html.parser")', type(soup), *dir(soup), type(soup).mro(), sep='\n', end='\n'*10)
    # CHECK find() -----------------------------------------------------------------------------------------------------

    if resp.status_code == 200:
        table = soup.find('table', id='ctl00_content_vacancyList_gridList')
        if table:
            tr_list = table.find_all('tr', attrs={'id': True}) # там id указаны как id="8360908" (любое другое число)

            # CHECK find() --------------------------------------------------------------------------------------------------------------
            print('soup.find("tag", attrs={"k":"v"})', type(table), *dir(table), type(table).mro(), sep='\n',
                  end='\n' * 10)
            # CHECK find() --------------------------------------------------------------------------------------------------------

            # CHECK find_all() -------------------------------------------------------------------------------------------------------
            print('soup.all_find("tag", attrs={"k":"v"})', type(tr_list),
                  *dir(tr_list), type(tr_list).mro(), sep='\n', end='\n'*10)
            # CHECK find_all() ---------------------------------------------------------------------------------------------------
        # print(*table, sep='\n'*15)

rabota_CHECK()

# print(*jobs,sep='\n')

# div_list (после метода find_all) - представляет из себя практически список. Но это не список.
# Это объект <class 'bs4.element.ResultSet'>
# метод find дает другой тип данных - <class 'bs4.element.Tag'>
# Ознакомься внимательно с тремя предыдущими строчками
# аттрибуты text и string достают текст между тегами (string если мало текста, text если много)
# -------------------------------------------------------------------------------------
# print(*dir(div_list), type(div_list),sep='\n')
# print(*div_list,sep='\n\n\n\n\n\n\n')
# print(type(div_list).mro()) # <class 'bs4.element.ResultSet'> унаследован от list
# -------------------------------------------------------------------------------------



with codecs.open('work.txt', 'w', 'utf-8') as f:
    f.write(str(jobs))



url_hh = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=python'

resp_hh = requests.get(url=url_hh, headers=headers)

# with codecs.open('hh_work.html', 'w', 'utf-8') as f:
#     f.write(str(resp_hh.text))

"""
    id="pjax-job-list"
"""