
import logging

from public import bp as public
from item import bp as item

logger = logging.getLogger('zgeist.web')

def register_all_blueprints(app):
    app.register_blueprint(item)
    app.register_blueprint(public)

