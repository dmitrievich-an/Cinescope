def greet(**kwargs):
    if "name" in kwargs and "age" in kwargs:
        return print(f"Hello, {kwargs["name"]}. You are {kwargs['age']} years old")
    if "name" in kwargs:
        return print(f"Hello, {kwargs["name"]}")
    if "age" in kwargs:
        return print(f"Hello! You are {kwargs['age']} years old")
    return print(f"Hello")


greet(name="Alice", age=25)


def create_dict(**kwargs):
    return kwargs


print(create_dict(a=1, b=2, c=3))

default_settings = {"theme": "light", "notifications": True}


def update_settings(def_set, **kwargs):
    def_set.update(kwargs)
    return def_set


print(update_settings(default_settings, theme="dark", volume=80))


def filter_kwargs(**kwargs):
    # filtered_kwargs = {}
    # for i in kwargs:
    #     if kwargs[i] > 10:
    #         filtered_kwargs.update({i: kwargs[i]})
    # return filtered_kwargs
    return {k: v for k, v in kwargs.items() if v > 10}


print(filter_kwargs(a=5, b=20, c=15, d=3))


def log_kwargs(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with kwargs: {kwargs}")
        return func(*args, **kwargs)

    return wrapper


@log_kwargs
def my_function(a, b, **kwargs):
    return a + b


my_function(5, 10, debug=True, verbose=False)
print(my_function(5, 10, debug=True, verbose=False))


def add_numbers(*numbers):
    return sum(numbers)


print(add_numbers(1, 2, 3))


def create_list(*item):
    return [i for i in item]


print(create_list(1, 2, 3))


def pass_arguments(*args):
    return print_args(*args)


def print_args(*args):
    for i in args:
        print(i)


pass_arguments(5, 7, 9)


def find_max(*nums):
    return max(nums)


print(find_max(5, 8, 13))


def join_strings(*strings):
    return " ".join(strings)


print(join_strings("Hello", "world", "!"))
