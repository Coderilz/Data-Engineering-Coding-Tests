from test_3 import sum_current_time

def test_works():
    time_str = '01:02:03'
    assert sum_current_time(time_str) == 6
