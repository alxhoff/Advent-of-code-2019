#!/bin/python


def get_digit(number, n):
    return number // 10**n % 10


def set_digit(number, n, value):
    cur_value = get_digit(number, n) * 10**n
    new_value = value * 10**n
    return number - cur_value + new_value


def increase_password(number):
    modified = False
    for i in range(5, -1, -1):
        digit = get_digit(number, i)
        next_digit = get_digit(number, i - 1)
        if next_digit < digit:
            modified = True
            for j in range(i + 1):
                number = set_digit(number, j, digit)
        elif i == 0 and not modified:
            if digit == 9:
                return increase_password(number + 1)
            else:
                return number + 1
    return number


def check_password(password):
    for i in range(5, 0, -1):
        cur_digit = get_digit(password, i)
        next_digit = get_digit(password, i - 1)
        if cur_digit == next_digit:
            if i == 1:
                if cur_digit != get_digit(password, i + 1):
                    return True
            if i == 5:
                if cur_digit != get_digit(password, i - 2):
                    return True
            else:
                if cur_digit != get_digit(password, i + 1) and next_digit != get_digit(password, i - 2):
                    return True
    return False


val = check_password(111199)

password_count = 0

#  lower_limit = int(input("Lower limit: "))
#  upper_limit = int(input("Upper limit: "))

lower_limit = 168630

if not check_password(lower_limit):
    lower_limit = increase_password(lower_limit)

upper_limit = 718098

current_password = lower_limit

while lower_limit <= current_password <= upper_limit:
    if check_password(current_password):
        password_count += 1
    current_password = increase_password(current_password)

print(password_count)
