from app import db
from app.main import bp
from app.models import Data
from app.main.forms import FilterForm

from bs4 import BeautifulSoup

from flask import render_template
from flask import request

from sqlalchemy import func

from time import time

import requests


@bp.route('/', methods=['GET'])
def index():
    """Основной контроллер, который обрабатывает запросы на фильтрацию и группировку
    информации из таблицы"""
    form = FilterForm()
    result_set = Data.query
    columns = [elem.name for elem in Data.__table__.columns if elem.name != 'timestamp']

    filters = {
        Data.date: [request.args.get('date_from'), 
                    request.args.get('date_to')],
        Data.keyword: request.args.get('kw'),
        Data.domain: request.args.get('domain', type=int),
        Data.code_response: request.args.get('code'),
        Data.size_page: request.args.get('size', type=int)
    }
    groups = {
        Data.date: request.args.get('g_date'),
        Data.keyword: request.args.get('g_kw'),
        Data.domain: request.args.get('g_domain'),
        Data.code_response: request.args.get('g_code')
    }



    if any(groups.values()):
        result_set = result_set.with_entities(*[key for key in groups if groups[key]], 
                                                func.sum(Data.size_page))
        columns = [desc['name'] for desc in result_set.column_descriptions if desc['name']]
        columns.append('sum_sizes')    
    for key in filters:
        if filters[key]:
            result_set = Data.filter(result_set, key, filters[key])

    if any(groups.values()):
        result_set = result_set.group_by(*[key for key in groups if groups[key]])
    
    result_set = result_set.all()
    if not isinstance(result_set, list):
        result_set = [result_set]
    return render_template('index.html', form=form, query=result_set, columns=columns)


@bp.route('/script')
def script():
    """Сбор данных для таблицы через поиск яндекса."""
    keyword = request.args.get('keyword')
    if not keyword:
        return 'I need keyword', 400
    r = requests.get(f'http://yandex.ru/?q={keyword}')
    soup = BeautifulSoup(r.content, 'lxml')
    headers = soup.find('body').find_all('h2')
    links = [headers[i].find('a')['href'] for i in range(len(headers)) if headers[i].find('a')]
    data = []
    for link in links:
        if link.startswith('http://yabs'):
            r = requests.get(link)
            soup = BeautifulSoup(r.content, 'lxml')
            url = soup.find('noscript').find('meta')['content'][7:-1]
            start = time()
            r = requests.get(url)
            finish = time() - start
        else:
            try:
                url = link
                start = time()
                r = requests.get(link)
                finish = time() - start
            except:
                continue
        data.append({'keyword': keyword, 'code_response': r.status_code, 'size_page': len(r.content),
                    'url': url, 'domain': r.headers.get('domain') or url, 'timeload': int(finish)})
    for elem in data:
        d = Data(**elem)
        db.session.add(d)
        db.session.commit()
    return 'OK', 200
    
    