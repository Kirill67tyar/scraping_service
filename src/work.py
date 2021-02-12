import requests
from bs4 import BeautifulSoup as BS
import codecs

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
           }


def record_errors(cause, resp, errors):
    errors.append({
        'url': url,
        'cause': cause,
        'status_code': resp.status_code,
    })

def get_jobs_erros_resp(url):
    resp = requests.get(url=url, headers=headers)
    jobs = []
    errors = []
    return jobs, errors, resp



def work(url):
    url = 'https://www.work.ua/ru/jobs-kyiv-python/'
    jobs, errors, resp = get_jobs_erros_resp(url)
    domain = 'https://www.work.ua'
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', id='pjax-job-list')
        if main_div:
            div_list = main_div.find_all('div', attrs={'class': 'job-link'})
            for div in div_list:
                title = div.find('h2')
                href = title.find('a')
                content = div.p.text#.strip()
                company = 'Unknown'
                if div.img:
                    company = div.img['alt']
                jobs.append({
                    'title': title.a.string,
                    'url': domain + href['href'],
                    'description': content,
                    'company': company
                })
        else:
            cause = 'Div does not exist'
            record_errors(cause=cause, resp=resp, errors=errors)
    else:
        cause = 'Page does not response'
        record_errors(cause=cause, resp=resp, errors=errors)
    return jobs, errors



def rabota(url):
    jobs, errors, resp = get_jobs_erros_resp(url)
    domain = 'https://rabota.ua'
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        new_jobs = soup.find('div', attrs={'class': 'f-vacancylist-newnotfound'})
        if not new_jobs:
            table = soup.find('table', id='ctl00_content_vacancyList_gridList')
            if table:
                tr_list = table.find_all('tr', attrs={'id': True}) # там id указаны как id="8360908" (любое другое число)
                for tr in tr_list:
                    div = tr.find('div', attrs={'class': 'card-body',}) # позволяет нам отсеить рекламные банеры
                    if div:
                        title = div.find('h2', attrs={'class': 'card-title'}) # не мой вариант
                        # title = div.h2.text.strip() # мой вариант
                        href = title.a['href']
                        # print(domain + href)
                        content = div.find('div', attrs={'class': 'card-description',}).text.strip()
                        # print(content,end='\n\n\n')
                        company = 'Unknown'
                        p = div.find('p', attrs={'class': 'company-name'})
                        if p:
                            company = p.a.text
                        jobs.append({
                            'title': title.text.strip(),
                            'url': domain+href,
                            'description': content,
                            'company': company,
                        })
                    else:
                        cause = 'Div does not exist'
                        record_errors(cause, resp=resp, errors=errors)

            else:
                cause = 'Table does not exist'
                record_errors(cause, resp=resp, errors=errors)

        else:
            cause = 'Page is empty'
            record_errors(cause, resp=resp, errors=errors)

    else:
        cause = 'Page does not response'
        record_errors(cause, resp=resp, errors=errors)
    return jobs, errors



def job_dou(url):
    url = 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python'
    jobs, errors, resp = get_jobs_erros_resp(url)
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', id='vacancyListId')
        if main_div:
            # ul = main_div.find('ul', attrs={'class': 'lt'})
            li_list = main_div.find_all('li', attrs={'class':'l-vacancy',})
            for li in li_list:

                if '__hot' not in li['class']:    # li['class'] = ['l-vacancy', '__hot']/['l-vacancy']
                    title = li.find('a', attrs={'class': 'vt'})
                    href = title['href']
                    content = li.find('div', attrs={'class': 'sh-info'}).text.strip()
                    company = 'Unknown'
                    comp = li.find('a', attrs={'class': 'company'}).text.strip()
                    if comp:
                        company = comp
                    jobs.append(
                        {'title': title.text.strip(),
                         'url': href,
                         'description': content,
                         'company': company,}
                    )
        else:
            cause = 'Div does not exist'
            record_errors(cause=cause, resp=resp, errors=errors)
    else:
        cause = 'Page does not response'
        record_errors(cause=cause, resp=resp, errors=errors)
    return jobs, errors



def djinni(url):
    # url = 'https://djinni.co/jobs/location-kyiv/?primary-keyword=Python'
    jobs, errors, resp = get_jobs_erros_resp(url)
    domain = 'https://djinni.co'
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_ul = soup.find('ul', attrs={'class': 'list-jobs',})
        # здесь мы ищем 'list-jobs' а не "list-unstyled list-jobs"
        # это связано с тем что list-unstyled с высокой вероятностью поменяется, list-jobs - более стабильна
        # это одна из фундаметнальных вещей работы с парсингом - пытаться взять или id тега или
        # минимум стабильной инфы
        if main_ul:
            li_list = main_ul.find_all('li', attrs={'class': 'list-jobs__item'})
            for li in li_list:
                title_href = li.find('div', attrs={'class': 'list-jobs__title'})
                title = title_href.text.strip()
                if '\n' in title:
                    title = title.split('\n')[0]
                href = domain + title_href.a['href']
                content = li.find('div', attrs={'class': 'list-jobs__description',}).text.strip()
                company = 'Unknown'
                detail_info = li.find('div', attrs={'class': 'list-jobs__details__info'})
                if detail_info:
                    company = detail_info.find('a', attrs={'style': True,}).text.strip()
                jobs.append(
                    {'title': title,
                    'url': href,
                    'description': content,
                    'company': company,}
                )
        else:
            cause = 'Ul does not exist'
            record_errors(cause=cause, resp=resp, errors=errors)
    else:
        cause = 'Page does not response'
        record_errors(cause=cause, resp=resp, errors=errors)
    return jobs, errors



"""
<li class="list-jobs__item">
<div class="inbox-date pull-right">сегодня</div>
<div class="list-jobs__title">
<a class="profile" href="/jobs/202358-wordpress-developer/">WordPress developer</a>
<span class="public-salary-item">$500-1000</span>
</div>
<div class="list-jobs__description">
<p>В команду веб-разработчиков :Dteam ищем WordPress developer. Наш  разработчик умеет быть самоорганизованным и очень скрупулёзным.</p>
</div>
<div class="list-jobs__details">
<a class="picture" href="/r/59963-hr-manager-at-dteam/">
<div class="recruiter-images-container">
<user-picture name="Елена Зуева" picture="https://p.djinni.co/2f/fdaf0cc2fbc5bea8c7e19e970c38c3/Logo_square_small_200.png" small="true"></user-picture>
</div>
</a>
<div class="list-jobs__details__info">
<a href="/r/59963-hr-manager-at-dteam/">Елена Зуева</a>,
      HR manager
      в 
      <a href="/jobs/company--dteam-c43fd/" style="color:#999;text-decoration:none;">:DTeam</a>
<br>
<i class="icon-location"></i> Киев <nobr>1 год опыта</nobr><nobr>Intermediate</nobr>
</br></div>
<span style="clear: both"></span>
</div>
</li>
"""



if __name__ == '__main__':
    url = 'https://djinni.co/jobs/location-kyiv/?primary-keyword=Python'
    jobs, errors = djinni(url)
    print(*jobs,errors,sep='\n')
    # url = 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python'
    # jobs, errors = job_dou(url)
    # print(*jobs,sep='\n')
#     url = 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2'
#     jobs, errors = rabota(url)
#     print(*jobs,errors,sep='\n')




# ---------------------------------------------------------------------------------------

# def work_hh():
#     jobs = []
#     errors = []
#     domain = 'https://hh.ru/vacancy/'
#     url = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=python'
#     resp = requests.get(url, headers=headers)
#     soup = BS(resp.content, 'html.parser')
#     if resp.status_code == 200:
#         div_list = soup.find('div', attrs={'class': 'vacancy-serp'})
#         # s = soup.find('div', attrs={'class': 'sticky-container',})
#         for record in div_list:
#             print(record, end='\n'*15)
#
#
# work_hh()




def record_work(jobs):
    with codecs.open('work.txt', 'w', 'utf-8') as f:
        f.write(str(jobs))


def record_hh_work():
    url_hh = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=python'

    resp_hh = requests.get(url=url_hh, headers=headers)
    # print(resp_hh.text, sep='\n' * 50)
    with codecs.open('hh_work.html', 'w', 'utf-8') as f:
        f.write(str(resp_hh.text))



"""

?location=Киев&primary-keyword=Python
"""