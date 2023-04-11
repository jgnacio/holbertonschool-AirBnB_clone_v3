from flask import Blueprint
app_views = Blueprint('views', __name__, template_folder='templates', url_prefix="/api/v1")
from api.v1.views.index import *

