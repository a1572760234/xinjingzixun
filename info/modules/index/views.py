from flask import render_template, session,current_app
from info.modules.index import index_bp

@index_bp.route('/index')
def index():
    session['name'] = 'python'
    return render_template('news/index.html')

@index_bp.route('/favicon.ico')
def get_favicon():
    return current_app.sent_static_file('/news/favicon.ico')