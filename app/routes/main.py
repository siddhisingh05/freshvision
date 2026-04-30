"""
main.py — Home and About page routes
Author: Siddhi Singh (Full-Stack Lead)
"""
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/about')
def about():
    return render_template('about.html')
