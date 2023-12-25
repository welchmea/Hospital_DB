from flask import Blueprint, render_template

index_page = Blueprint('main_page', __name__)

# Routes - main navigation of site at index
@index_page.route('/')
def index():
    return render_template("index.html")