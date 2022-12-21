from translator.mlworker import work
import multiprocessing

job_queue = multiprocessing.Queue()

def start_threads(num_threads, db, slowstart=False):
    # Check the database to see if any items were processing on last shutdown.
    translations_processing = db.find({'status.message': "PROCESSING"}, {'_id': 1})
    for translation in translations_processing:
        id = str(translation['_id'])
        print(f"Restored job {id} to queue! (Was PROCESSING)")
        job_queue.put(id)

    # Check the database to see if any items were in queue on last shutdown.
    translations_in_queue = db.find({'status.message': "IN_QUEUE"}, {'_id': 1})
    for translation in translations_in_queue:
        id = str(translation['_id'])
        print(f"Restored job {id} to queue! (Was IN_QUEUE)")
        job_queue.put(id)

    # Compute a delay amount between threads starting to ensure even spacing.
    delay = 30 if slowstart else 1.0/float(num_threads)

    processes = []

    # Create and start the number of threads requested.
    for i in range(num_threads):
        process = multiprocessing.Process(target=work, args=(i, job_queue, i*delay, db, -1))
        process.start()
        processes.append(process)

    return processes
