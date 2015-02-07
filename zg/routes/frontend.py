"""
Frontend Routes
"""

from __future__ import division, print_function, absolute_import, unicode_literals
from flask import Blueprint, g, jsonify, abort, request, redirect, render_template, url_for, session
from zg.forms.item import CreateForm
from zg.objects import Tag

frontend = Blueprint('frontend', __name__)

@frontend.route('/upload')
def upload():
    form = CreateForm()
    return render_template('item/create.html', form=form)

@frontend.route('/tag/suggest')
def tag_suggest():
    """
    Item tag suggestions.

    Receives a query (``q`` parameter string) and preforms a search
    for tags that include the string in their name.
    Returns a json object with a ``tags`` key, a array of tag names.
    """
    return jsonify(tags=[tag.name for tag in Tag.suggest(request.args['q'])])


