import meta_data
import music_data
import pattern_data
import state_machine
import curcur
# main.py
import concurrent.futures
import time
from music_data import notes, scales, time_value_durations
from pattern_data import drum_pattern
import midi_in
import midi_out



# Something pick


# 



# Number of items to process
TOTAL_ITEMS = int(input("Enter the number of items to process:"))
CHUNK_SIZE = 10_000_000  # How many items each worker processes at once

def process_in_chunks(start, end):
    # Call the worker function to process a chunk of data
    result = worker.process_data(start, end)
    return result

def main():
    # Define the range of chunks that will be processed
    start_time = time.time()

    # Use a ProcessPoolExecutor to parallelize the work
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Split work into chunks and submit jobs for processing
        futures = []
        for start in range(0, TOTAL_ITEMS, CHUNK_SIZE):
            end = min(start + CHUNK_SIZE - 1, TOTAL_ITEMS - 1)
            futures.append(executor.submit(process_in_chunks, start, end))
        
        # Collect the results as they finish
        results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            print(f"Finished: {result}")

    # No longer saving results to a JSON file
    pass

    end_time = time.time()
    print(f"Total time taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    main()

