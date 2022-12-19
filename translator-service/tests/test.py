import pytest
import mongomock
from translator.util import supported_languages
import multiprocessing
from bson.objectid import ObjectId
import time
from translator import mlfunctions, mlworker
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

ckpt = 'facebook/m2m100_418M'

# Load files to variables
test_langs = ['arabic', 'english', 'hindi', 'portuguese', 'spanish']
inputs = {}
for lang in test_langs:
    file = open(f"tests/files/{lang}.wav", "rb")
    inputs[lang] = file.read()
    file.close()

@pytest.mark.parametrize("text,output_lang,expected_output", [
    ("hello", "fr", "Bonjour"),
    ("goodbye", "de", "Abschied"),
    ("how are you?", "es", "¿Cómo estás tú?"),
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
    db = mongomock.MongoClient('mongodb://localhost:27017')
    yield db.translator.translations
    # Clean up any changes made to the test database

@pytest.fixture
def model_tr():
    yield M2M100ForConditionalGeneration.from_pretrained(ckpt)

@pytest.fixture
def tokenizers():
    yield {lang: M2M100Tokenizer.from_pretrained(ckpt, src_lang="en", tr_lang=lang) for lang in supported_languages}

@pytest.fixture
def job_queue():
    queue = multiprocessing.Queue()
    yield queue

@pytest.mark.parametrize("lang,expected_output", [
    ('arabic', "Assalam Alaikum"),
    ('english', "The book is on the table."),
    ('hindi', "I am studying"),
    ('portuguese', "I like to eat bananas."),
    ('spanish', "Where is the library?")
])
def test_work(lang, expected_output, test_db, job_queue):
    # Set up job in the database for the worker to process, add to queue.
    job_id = str(test_db.insert_one({
        "user": None,
        "translation": {
            "outputLanguage": "en"
        },
        "status": {
            "message": "IN_QUEUE",
            "update": time.time()
        },
        "body": inputs[lang]
    }).inserted_id)
    job_queue.put(job_id)

    # Use the main thread to go through the queue.
    mlworker.work(0, job_queue, 0, test_db, 4)

    # Check that the output in the database matches the expected output
    result = test_db.find_one({'_id': ObjectId(job_id)})
    assert result['translation']['outputText'] == expected_output

# def test_add_job():
#     #test when outputLanguage is in acceptable languages
#     response = add_job(outputLanguage="en")
#     assert response.status_code == 200
#     assert "IN_QUEUE" in response.body

#     #est when outputLanguage is not in acceptable languages
#     response = add_job(outputLanguage="fr")
#     assert response.status_code == 400
#     assert "outputLanguage not in acceptable languages!" in response.body

#     #test with userId
#     response = add_job(outputLanguage="en", userId="123")
#     assert response.status_code == 200
#     assert "IN_QUEUE" in response.body
#     assert "123" in response.body

#     #test with empty userId
#     response = add_job(outputLanguage="en", userId="")
#     assert response.status_code == 200
#     assert "IN_QUEUE" in response.body
#     assert "None" in response.body

