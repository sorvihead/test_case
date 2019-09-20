from app import db
from datetime import date
from datetime import datetime
from time import time


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=date.today, index=True)
    timestamp = db.Column(db.Time, default=datetime.utcnow().time)
    keyword = db.Column(db.String(50), index=True)
    url = db.Column(db.String(200), index=True)
    domain = db.Column(db.String(100), index=True)
    timeload = db.Column(db.Integer, index=True)
    code_response = db.Column(db.Integer, index=True)
    size_page = db.Column(db.Integer, index=True)

    def __repr__(self):
        return f'<{self.id}, {self.date}, {self.keyword}, {self.url}, {self.domain}, {self.timeload}, {self.code_response}, {self.size_page}>'

    @classmethod
    def filter(cls, query, column, flt):
        if not flt:
            return query
        else:
            if column is Data.date:
                return cls.filter_date(query, *flt)
            elif column is Data.keyword:
                return cls.filter_keyword(query, flt)
            elif column is Data.domain:
                return cls.filter_domain(query, flt)
            elif column is Data.code_response:
                return cls.filter_code(query, flt)
            elif column is Data.size_page:
                return cls.filter_size(query, flt)

    @classmethod
    def filter_date(cls, query, date_from, date_to):
        return query.filter(Data.date.between(date_from, date_to))

    @classmethod
    def filter_keyword(cls, query, keyword):
        return query.filter(Data.keyword.contains(keyword))

    @classmethod
    def filter_domain(cls, query, domain):
        return query.filter_by(domain=domain)

    @classmethod    
    def filter_code(cls, query, code):
        if isinstance(code, int):
            return query.filter_by(code_response=code)
        elif len(code) == 3 and code[1::] in 'xxXX':
            try:
                code = (int(code[0]*100), int(code[0]*100)+99)
            except ValueError:
                return query

            return query.filter(Data.code_response.in_(code))
        else:
            return query

    @classmethod    
    def filter_size(cls, query, size):
        return query.filter(Data.size_page >= size) 
    
