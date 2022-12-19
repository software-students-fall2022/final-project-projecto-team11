import translator.mlfunctions
from translator.util import supported_languages
from bson.objectid import ObjectId
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import time
import whisper
import warnings
import torch
import traceback

def work(tid, job_queue, delay, db, retryLimit):
    # Wait for a delay to allow for even spacing between threads.
    time.sleep(delay)

    # Load ML models.
    warnings.filterwarnings("ignore", category=UserWarning) # Block out warnings about machine preferences.
    print(f"THREAD {tid}: Started loading ML models.")
    ckpt = 'facebook/m2m100_418M'
    model_tr = M2M100ForConditionalGeneration.from_pretrained(ckpt)
    toks = {lang: M2M100Tokenizer.from_pretrained(ckpt, src_lang="en", tr_lang=lang) for lang in supported_languages}
    # Check if CUDA is available for faster processing, if so enable CUDA.
    device = 'cuda' if torch.cuda.is_available() else None
    whisper_model = whisper.load_model(name='base', device=device)
    print(f"THREAD {tid}: Finished loading ML models.")

    retries = 0

    while retryLimit > retries or retryLimit == -1:
        # If no jobs in queue, wait one second, then check again.
        if job_queue.qsize() == 0:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                # If user tries to exit the program, gracefully exit.
                break
            retries += 1
            continue

        retries = 0
        
        # Otherwise, pull a job from the queue and start processing it.
        job = job_queue.get()
        try:
            print(f"THREAD {tid}: Found job with ID {job}.")
            # Get translation object from db, do not return body field.
            translation_cursor = db.find({'_id': ObjectId(job)})
            translation = translation_cursor.next()

            # Update translation status to PROCESSING.
            db.update_one({'_id': ObjectId(job)}, {'$set': {
                'status': {
                    'message': "PROCESSING",
                    'update': time.time()
                }
            }})

            # Handle transcription and translation.
            print(f"THREAD {tid}: Started processing job {job}.")
            output_language = translation['translation']['outputLanguage']
            transcription = translator.mlfunctions.transcribe(job, translation['body'], whisper_model)
            translated_message = transcription['english_text']
            if output_language != "en":
                translated_message = translator.mlfunctions.translate(translated_message, output_language, model_tr, toks)

            # Update translation status to SUCCESS and add translation information.
            db.update_one({'_id': ObjectId(job)}, {'$set': {
                'translation': {
                    'inputLanguage': transcription['input_language'],
                    'inputText': transcription['input_text'],
                    'outputLanguage': output_language,
                    'outputText': translated_message
                },
                'status': {
                    'message': "SUCCESS",
                    'update': time.time()
                },
                'body': None
            }})
            print(f"THREAD {tid}: Finished processing job: {job}.")
        except StopIteration:
            print(f"Job with ID {job} not found in database!")
        except KeyboardInterrupt:
            print(f"KeyboardInterrupt while processing job {job}!")
        except:
            print(f"Unknown error when processing job {job}!")
            traceback.print_exc()
            # Update translation status to FAILURE.
            db.update_one({'_id': ObjectId(job)}, {'$set': {
                'status': {
                    'message': "FAILURE",
                    'update': time.time()
                },
                'body': None
            }})
