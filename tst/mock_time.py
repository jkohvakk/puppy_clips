mock_sleep_calls = 0
mock_sleep_times = []


def reset():
    global mock_sleep_calls
    global mock_sleep_times
    mock_sleep_calls = 0
    mock_sleep_times = []


def get_mock_sleep_calls():
    return mock_sleep_calls


def get_mock_sleep_times():
    return mock_sleep_times


def sleep(seconds):
    global mock_sleep_calls
    mock_sleep_calls += 1
    mock_sleep_times.append(seconds)

def strftime(*args, **kwargs):
    return '2015.01.31-20:10'

