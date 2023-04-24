import time

def assert_with_time_out(func, time_out):
    start = time.time()
    result = None
    while not result:
        try:
            result = func()
        except:
            end = time.time()
            if end - start > time_out:
                raise Exception("Wrong test case")
            time.sleep(0.1)
