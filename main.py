import threading
import random
import time

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

# Shared resources
stack = []
mutex = threading.Lock()
all_file = open("all.txt", "w")
even_file = open("even.txt", "w")
odd_file = open("odd.txt", "w")

def producer():
    for _ in range(MAX_COUNT):
        num = random.randint(LOWER_NUM, UPPER_NUM)
        with mutex:
            stack.append(num)
            all_file.write(f"{num}\n")

def consumer_even():
    count = 0
    while count < MAX_COUNT:
        with mutex:
            if stack and stack[-1] % 2 == 0:
                num = stack.pop()
                even_file.write(f"{num}\n")
                count += 1

def consumer_odd():
    count = 0
    while count < MAX_COUNT:
        with mutex:
            if stack and stack[-1] % 2 != 0:
                num = stack.pop()
                odd_file.write(f"{num}\n")
                count += 1

def main():
    start_time = time.time()

    # Create threads
    producer_thread = threading.Thread(target=producer)
    consumer_even_thread = threading.Thread(target=consumer_even)
    consumer_odd_thread = threading.Thread(target=consumer_odd)

    # Start threads
    producer_thread.start()
    consumer_even_thread.start()
    consumer_odd_thread.start()

    # Join threads
    producer_thread.join()
    consumer_even_thread.join()
    consumer_odd_thread.join()

    # Close files
    all_file.close()
    even_file.close()
    odd_file.close()

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time} seconds")

if __name__ == "__main__":
    main()
