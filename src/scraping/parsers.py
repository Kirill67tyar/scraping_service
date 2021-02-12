import requests
from bs4 import BeautifulSoup as BS
import codecs
from random import choice

__all__ = ('work', 'rabota', 'job_dou', 'djinni',)

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},

    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},

    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
           ]


def record_errors(url, cause, resp, errors):
    errors.append({
        'url': url,
        'cause': cause,
        'status_code': resp.status_code,
    })

def get_jobs_erros_resp(url):
    resp = requests.get(url=url, headers=choice(headers))
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
            record_errors(url=url, cause=cause, resp=resp, errors=errors)
    else:
        cause = 'Page does not response'
        record_errors(url=url, cause=cause, resp=resp, errors=errors)
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
                        record_errors(url=url, cause=cause, resp=resp, errors=errors)

            else:
                cause = 'Table does not exist'
                record_errors(url=url, cause=cause, resp=resp, errors=errors)

        else:
            cause = 'Page is empty'
            record_errors(url=url, cause=cause, resp=resp, errors=errors)

    else:
        cause = 'Page does not response'
        record_errors(url=url, cause=cause, resp=resp, errors=errors)
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
            record_errors(url=url, cause=cause, resp=resp, errors=errors)
    else:
        cause = 'Page does not response'
        record_errors(url=url, cause=cause, resp=resp, errors=errors)
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
        # минимум стабильной инфы. Похоже на бритву оккама - минимум, но достаточной инфы
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
            record_errors(url=url, cause=cause, resp=resp, errors=errors)
    else:
        cause = 'Page does not response'
        record_errors(url=url, cause=cause, resp=resp, errors=errors)
    return jobs, errors



def record_work(jobs):
    with codecs.open('work.txt', 'w', 'utf-8') as f:
        f.write(str(jobs))


def record_hh_work():
    url_hh = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=python'

    resp_hh = requests.get(url=url_hh, headers=headers)
    # print(resp_hh.text, sep='\n' * 50)
    with codecs.open('hh_work.html', 'w', 'utf-8') as f:
        f.write(str(resp_hh.text))





if __name__ == '__main__':
    url = 'https://djinni.co/jobs/location-kyiv/?primary-keyword=Python'
    jobs, errors = djinni(url)
    print(*jobs,errors,sep='\n')
    # url = 'https://jobs.dou.ua/vacancies/?city=%D0%9A%D0%B8%D0%B5%D0%B2&category=Python'
    # url = 'https://rabota.ua/zapros/python/%d0%ba%d0%b8%d0%b5%d0%b2'



