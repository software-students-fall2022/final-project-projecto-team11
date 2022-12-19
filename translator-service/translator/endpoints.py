from flask import request, jsonify, redirect, url_for
from bson.objectid import ObjectId
from translator.jobhandler import default_job_queue
from translator.util import db, supported_languages
import time

def add_job():
    # Check that language is supported.
    language = request.args.get('outputLanguage')
    if language != "en" and language not in supported_languages:
        return "outputLanguage not in acceptable languages!", 400

    # Get user ID if it exists, and add it to the translation.
    user = request.args.get('userId')
    user = None if user=='' else user

    # Create a new translation object with the data received.
    translation = {
        "user": user,
        "translation": {
            "outputLanguage": language
        },
        "status": {
            "message": "IN_QUEUE",
            "update": time.time()
        },
        "body": request.data
    }
    result = db.insert_one(translation)
    default_job_queue.put(result.inserted_id)
    return redirect(url_for("get_job", id=str(result.inserted_id)))

def get_job(id):
    try:
        # Get translation object from db, do not return body field.
        translation_cursor = db.find({'_id': ObjectId(id)}, {'body': 0})
        translation = translation_cursor.next()
        # Stringify translation ID and user ID before returning to user.
        translation['_id'] = str(translation['_id'])
        # TODO: Stringify user ID before returning to user.
        # Find what HTTP code to return based off translation job status.
        status = 500 if translation['status']['message'] == "FAILURE" else 200
        # Return all translation information as JSON, with correct HTTP code.
        return jsonify(translation), status
    except StopIteration:
        return "No translation found with that ID.", 404
