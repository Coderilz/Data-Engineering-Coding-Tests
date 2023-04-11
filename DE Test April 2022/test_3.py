# The below function doesn't work correctly. It should sum all the numbers at the
# current time. For example, 01:02:03 should return 6. Improve and fix the function,
# and write unit test(s) for it. Use any testing framework you're familiar with.


# [TODO]: fix the function
def sum_current_time(time_str: str) -> int:
    """Expects data in the format HH:MM:SS"""
    str_list_of_nums = time_str.split(":")

    int_list_of_nums = [int(x) for x in str_list_of_nums]

    return sum(int_list_of_nums)

def test_works():
    time_str = '01:02:03'
    assert sum_current_time(time_str) == 6
