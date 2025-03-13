from flask import Blueprint, render_template

bp = Blueprint('home', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/team')
def team():
    return render_template('team_page.html')
