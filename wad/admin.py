#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Admin'''

import os

import plist
import db

from io import BytesIO
from datetime import datetime
from flask import Blueprint, render_template
from flask import jsonify, request, current_app, abort
from werkzeug.utils import secure_filename

admin_app = Blueprint('admin', __name__)  # pylint: disable=C0103

@admin_app.route('/')
def index():
    '''Index'''

    return render_template('admin.html')


def parse_ipa(file_path):
    '''Parse IPA'''

    try:
        info = plist.get_info(file_path)
    except (IOError, NameError):
        return None

    return info


def save_to_database(info):
    '''Save ipa info to database'''

    archive = db.Archive(**info)
    archive.date = datetime.now()
    archive.save()


@admin_app.route('/upload', methods=['GET', 'POST'])
def upload():
    '''File upload'''

    if request.method == 'POST':
        ipa = request.files['ipa_file']
        if not ipa:
            return jsonify(error=1, message='No IPA file')

        info = parse_ipa(BytesIO(ipa.read()))
        if not info:
            return jsonify(error=2, message='Fail to parse IPA file')

        # Save file
        file_name = secure_filename(ipa.filename)
        ipa.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file_name))

        info['path'] = file_name

        save_to_database(info)

    return jsonify(error=0, info=info)


@admin_app.route('/archives')
def get_all_archives():
    '''Get all archives'''

    # query parameters
    identifier = request.args.get('identifier', None)

    archives = db.get_archives(identifier=identifier)
    return jsonify(archives=archives)


@admin_app.route('/archives/<archive_id>', methods=['GET', 'PUT', 'DELETE'])
def get_single_archvie(archive_id):
    '''Get single archive'''

    archive = db.get_archvie_by_id(archive_id)
    if not archive:
        abort(404)

    if request.method == 'GET':
        return jsonify(archive=archive.dict_format())
    elif request.method == 'DELETE':
        archive.delete_instance()
    elif request.method == 'PUT':
        # publish
        pass

    return jsonify(error=0)
