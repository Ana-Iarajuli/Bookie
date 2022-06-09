from flask import Blueprint

admin_page = Blueprint('admin', __name__)

@admin_page.route('/')
def home():
    return 'admin hoome page'

@admin_page.route('/user')
def user():
    return 'user home page'