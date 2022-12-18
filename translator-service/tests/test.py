import pytest
import threading
import time
import translator.mlfunctions
from translator.util import db, supported_languages
from bson.objectid import ObjectId
from translator import mlfunctions

@pytest.mark.parametrize("text,output_lang,expected_output", [
    ("hello", "fr", "bonjour"),
    ("goodbye", "de", "auf wiedersehen"),
    ("how are you?", "es", "¿cómo estás?"),
])
def test_translate(text, output_lang, expected_output, model_tr, tokenizers):
    # Ensure that the function returns the expected translation for various input phrases
    assert mlfunctions.translate(text, output_lang, model_tr, tokenizers) == expected_output

def test_translate_unsupported_language(model_tr, tokenizers):
    # Ensure that the function raises a KeyError when given an unsupported language
    with pytest.raises(KeyError):
        mlfunctions.translate("hello", "xyz", model_tr, tokenizers)

@pytest.fixture
def test_db():
    # Set up a test database for the duration of the test
    # You may need to modify this to create a new database or collection specifically for the test
    yield db
    # Clean up any changes made to the test database

@pytest.mark.parametrize("tid,delay,input_data,expected_output", [
    (1, 0, b"Hello", {'english_text': 'Hello', 'input_language': 'en', 'input_text': 'Hello'}),
    (2, 1, b"Bonjour", {'english_text': 'Hello', 'input_language': 'fr', 'input_text': 'Bonjour'}),
    (3, 2, b"Hola", {'english_text': 'Hello', 'input_language': 'es', 'input_text': 'Hola'}),
])
def test_work(tid, delay, input_data, expected_output, test_db):
    # Set up a job in the database for the worker to process
    job_id = test_db.insert_one({'body': input_data}).inserted_id

    # Create a job queue and add the job to it
    job_queue = queue.Queue()
    job_queue.put(str(job_id))

    # Create a worker thread and start it
    worker = threading.Thread(target=translator.mlfunctions.work, args=(tid, job_queue, delay))
    worker.start()

    # Wait for the worker to finish processing the job
    worker.join()

    # Check that the output in the database matches the expected output
    result = test_db.find_one({'_id': job_id})
    assert result['translation'] == expected_output
    assert result['status']['message'] == "SUCCESS"




