from flask import url_for, current_app, render_template, jsonify, request

from app import db
from app.main import bp
from app.models import Data
from app.main.forms import FilterForm

from sqlalchemy import func


@bp.route('/', methods=['GET'])
def index():
    form = FilterForm()
    filters = {
        Data.date: request.args.get('date'),
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

    result_set = Data.query

    if any(groups.values()):
        result_set = result_set.with_entities(*[key for key in groups if groups[key]], 
                                                func.sum(Data.size_page))

    
    for key in filters:
        result_set = Data.filter(result_set, key, filters[key])

    if any(groups.values()):
        result_set = result_set.group_by(*[key for key in groups if groups[key]])
    result_set = result_set.all()
    return render_template('index.html', form=form, query=result_set)

    