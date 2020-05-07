# Totally basic code to pass first day in sushi go round
# Script made to learn python
# Only first two day of game covered
# 07/05/2020 07:30 Piotr Rogalski

# TODO: Day 3
# TODO: Investigate bug when game adds less resources than delcared 10 or 5 (for example 8 instead of 10)

import pyautogui
import os
import time
import functools

mouseIdle = (100, 250)
list_res_ordered = []
basicObjects = {}
dict_res = dict(rice=10,
                nori=10,
                roe=10,
                salmon=5,
                shrimp=5,
                unagi=5)

gameStarted = False

os.chdir(r'E:\DropBox\Dropbox\Elektronika\Programowanie\Python\SushiGoRound\assets')


def wrapper(func):
    def function(*args, **kwargs):
        start = time.time()
        print('-' * 30)
        print("Executing: {}".format(func.__name__))
        print("Args: ")
        print(args)
        print("Kwargs: ")
        print(kwargs)
        result = func(*args, **kwargs)
        print("Returned: {}".format(result))
        print("Execution time: {}".format(time.time() - start))
        return result

    return function


# This function starts game and maps some basic object on the screen
def start_game():
    # Determining game aera
    top = pyautogui.locateOnScreen('top.png')
    bottom = pyautogui.locateOnScreen('bottom.png')
    work_area = (bottom[0], top[1], bottom[0] + bottom[2], bottom[1] + bottom[3])

    # Starting the game
    click_on_match('play.png', work_area)
    click_on_match('continue.png', work_area)
    click_on_match('skip.png', work_area)
    click_on_match('continue.png', work_area)

    # Mapping basic objects in the screen and saving them to the dictionary
    dict_map = dict(screen=work_area,
                    res_rice=pyautogui.locateCenterOnScreen('rice.png', region=work_area),
                    res_nori=pyautogui.locateCenterOnScreen('nori.png', region=work_area),
                    res_roe=pyautogui.locateCenterOnScreen('roe.png', region=work_area),
                    res_salmon=pyautogui.locateCenterOnScreen('salmon.png', region=work_area),
                    phone=pyautogui.locateCenterOnScreen('phone.png', region=work_area),
                    deliver=pyautogui.locateCenterOnScreen('empty_table.png', region=work_area))

    # Mapping inital phone menu
    pyautogui.click(dict_map['phone'])
    dict_map['select_rice'] = pyautogui.locateCenterOnScreen('select_rice.png', region=work_area)
    dict_map['select_other'] = pyautogui.locateCenterOnScreen('select_other.png', region=work_area)
    click_on_match('terminate_call.png', work_area)

    # Returning dictionary filled with coordinates of basic objects on the screen
    return dict_map


# This function checks if game day has finished and starts new day
def check_next_level(area):
    global dict_res
    if pyautogui.locateOnScreen('win.png', region=area) is None:
        return False
    start = time.time()
    while True:
        if start + 10 <= time.time():
            click_on_match('continue.png', area)
            click_on_match('continue.png', area)
            dict_res['rice'] = 10
            dict_res['nori'] = 10
            dict_res['roe'] = 10
            dict_res['salmon'] = 5
            dict_res['shrimp'] = 5
            dict_res['unagi'] = 5

            return True


def click_on_match(pattern, area, timeout=1):
    start = time.time()
    coordinates = pyautogui.locateCenterOnScreen(pattern, region=area)
    while coordinates is None:
        coordinates = pyautogui.locateCenterOnScreen(pattern, region=area)
        if start + timeout < time.time():
            return False
    pyautogui.click(coordinates)
    pyautogui.moveTo(mouseIdle)


def click_on_match_if_possible(pattern, area):
    coordinates = pyautogui.locateCenterOnScreen(pattern, region=area)
    if coordinates is not None:
        pyautogui.click(coordinates)
        return True
    return False


def wait_for_match(pattern, area, timeout=1):
    start = time.time()
    while pyautogui.locateCenterOnScreen(pattern, region=area) is None:
        if start + timeout < time.time():
            return False
    return True


def check_if_match(pattern, area):
    coordinates = pyautogui.locateCenterOnScreen(pattern, region=area)
    if coordinates is not None:
        return coordinates
    else:
        return False


# This function tries to order new resources if possible, returns ordered resource and a timestamp or None
def order(resource, objects):
    pyautogui.click(objects['phone'])
    if resource == 'rice':
        pyautogui.click(objects['select_rice'])
    else:
        pyautogui.click(objects['select_other'])
    coordinates = check_if_match('{}_order.png'.format(resource), objects['screen'])
    if coordinates is not False:
        pyautogui.click(coordinates)
        click_on_match('free_order.png', objects['screen'])
        return [resource, time.time()]
    else:
        click_on_match('terminate_call.png', objects['screen'])
        return None


def resupply(resource, minimum, objects):
    global dict_res
    global list_res_ordered
    if dict_res[resource] <= minimum:
        for entry in list_res_ordered:
            if entry[0] == resource:
                return
        result = order(resource, objects)
        if result is None:
            return
        list_res_ordered.append(result)
        return True
    return False


# Game bug may be here - sometimes game add less resources than declared
def warehouse_keeper():
    global dict_res
    global list_res_ordered
    if not list_res_ordered:
        return
    remove_list = []
    time_delay = 5
    for i in range(len(list_res_ordered)):
        if list_res_ordered[i][1] + time_delay < time.time():
            if list_res_ordered[i][0] == 'shrimp' or list_res_ordered[i][0] == 'salmon' or list_res_ordered[i][0] == 'unagi':
                dict_res[list_res_ordered[i][0]] += 5
                print("Adding 5 to {} now: {}".format(list_res_ordered[i][0], dict_res[list_res_ordered[i][0]]))
            else:
                dict_res[list_res_ordered[i][0]] += 10
                print("Adding 10 to {} now: {}".format(list_res_ordered[i][0], dict_res[list_res_ordered[i][0]]))
            remove_list.append(i)
    num_elems_to_remove = len(remove_list) - 1
    for j in range(num_elems_to_remove, -1, -1):
        list_res_ordered.pop(remove_list[j])


def prepare_onigiri(objects):
    global dict_res
    if dict_res['rice'] < 2 or dict_res['nori'] < 1:
        return False
    if not wait_for_match('empty_table.png', objects['screen']):
        return False
    pyautogui.doubleClick(objects['res_rice'])
    dict_res['rice'] -= 2
    pyautogui.click(objects['res_nori'])
    dict_res['nori'] -= 1
    pyautogui.click(objects['deliver'])
    return True


def prepare_california_roll(objects):
    global dict_res
    if dict_res['rice'] < 1 or dict_res['nori'] < 1 or dict_res['roe'] < 1:
        return False
    if not wait_for_match('empty_table.png', objects['screen']):
        return False
    pyautogui.click(objects['res_rice'])
    dict_res['rice'] -= 1
    pyautogui.click(objects['res_nori'])
    dict_res['nori'] -= 1
    pyautogui.click(objects['res_roe'])
    dict_res['roe'] -= 1
    pyautogui.click(objects['deliver'])
    return True


def prepare_gunkan_maki(objects):
    global dict_res
    if dict_res['rice'] < 1 or dict_res['nori'] < 1 or dict_res['roe'] < 2:
        return False
    if not wait_for_match('empty_table.png', objects['screen']):
        return False
    pyautogui.click(objects['res_rice'])
    dict_res['rice'] -= 1
    pyautogui.click(objects['res_nori'])
    dict_res['nori'] -= 1
    pyautogui.doubleClick(objects['res_roe'])
    dict_res['roe'] -= 2
    pyautogui.click(objects['deliver'])
    return True


def prepare_salmon_roll(objects):
    global dict_res
    if dict_res['rice'] < 1 or dict_res['nori'] < 1 or dict_res['salmon'] < 2:
        return False
    if not wait_for_match('empty_table.png', objects['screen']):
        return False
    pyautogui.click(objects['res_rice'])
    dict_res['rice'] -= 1
    pyautogui.click(objects['res_nori'])
    dict_res['nori'] -= 1
    pyautogui.doubleClick(objects['res_salmon'])
    dict_res['salmon'] -= 2
    pyautogui.click(objects['deliver'])
    return True


def prepare_meal(meal, objects):
    if meal == 'onigiri':
        return prepare_onigiri(objects)
    elif meal == 'california_roll':
        return prepare_california_roll(objects)
    elif meal == 'gunkan_maki':
        return prepare_gunkan_maki(objects)
    elif meal == 'salmon_roll':
        return prepare_salmon_roll(objects)


def check_orders_and_prepare_meals(meal, objects):
    orders = len(list(pyautogui.locateAllOnScreen(meal + '_customer.png')))
    prepared = len(list(pyautogui.locateAllOnScreen(meal + '_on_belt.png')))
    to_prepare = orders - prepared
    if to_prepare < 0:
        to_prepare = 0
    for i in range(to_prepare):
        prepare_meal(meal, objects)


def empty_plates(area):
    for i in range(1, 8):
        click_on_match_if_possible('plate{}.png'.format(i), area)


basicObjects = start_game()

while True:
    warehouse_keeper()
    check_orders_and_prepare_meals('onigiri', basicObjects)
    check_orders_and_prepare_meals('california_roll', basicObjects)
    check_orders_and_prepare_meals('gunkan_maki', basicObjects)
    check_orders_and_prepare_meals('salmon_roll', basicObjects)
    empty_plates(basicObjects['screen'])
    resupply('rice', 7, basicObjects)
    resupply('nori', 7, basicObjects)
    resupply('roe', 7, basicObjects)
    resupply('salmon', 4, basicObjects)
    warehouse_keeper()
    empty_plates(basicObjects['screen'])
    check_next_level(basicObjects['screen'])
