from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, BooleanField
from wtforms.validators import Optional
from datetime import date

class FilterForm(FlaskForm):
    g_date = BooleanField(
        "Group date",
        validators=(Optional(), )
    )
    date = DateField(
        'Date', 
        format='%y/%m/%d', 
        validators=(Optional(), ),
        render_kw={"type": "date"},
        default=date.today()
    )
    g_kw = BooleanField(
        "Group keyword",
        validators=(Optional(), )
    )
    kw = StringField(
        'Keyword',
        validators=(Optional(), ),
        render_kw={"size": 100},
        default=''
    )
    g_domain = BooleanField(
        "Group domain",
        validators=(Optional(), )
    )
    domain = StringField(
        'Domain',
        validators=(Optional(), ),
        render_kw={"size": 100},
        default=''
    )
    g_code = BooleanField(
        "Group code",
        validators=(Optional(), )
    )
    code = StringField(
        'Code of response',
        validators=(Optional(), ),
        render_kw={"size": 100},
        default=''
    )
    size = StringField(
        'Size of page',
        validators=(Optional(), ),
        render_kw={"size": 100},
        default=''
    )
    submit = SubmitField('Go')
    reset = SubmitField(
        'Reset',
        render_kw={"type": "reset"}
    )
