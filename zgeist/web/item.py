# -*- coding: utf-8 -*-

import logging

from flask import Blueprint, g, jsonify, abort, request, redirect, render_template, url_for, session

from zgeist.form import CreateForm
import zgeist.task as task
from zgeist.model import Item
import zgeist.util as util

logger = logging.getLogger('zgeist.web')

bp = Blueprint('item', __name__, template_folder='templates')

@bp.route('/item/create', methods=['GET', 'POST'])
def create():
    form = CreateForm(request.form)
    if request.method == 'POST' and form.validate():
        logger.debug('create form posted, creating empty item')
        item = Item.create(form.title.data, form.description.data)

        if form.group.data:
            task.url.discover.delay(item.id, form.urls.data)
        else:
            map(lambda url: task.url.discover.delay(item.id, [url]), form.urls.data)

    return render_template('item/create.html', form=form)

