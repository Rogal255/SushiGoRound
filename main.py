# Totally basic code to pass first day in sushi go round
# Script made to learn python
# Only first day of game covered
# 06/05/2020 08:10 Piotr Rogalski

# TODO: Sushi making based on orders rather than upfront randomly
# TODO: Time control

import pyautogui
import os
import time

mouseIdle = (100, 100)
basicObjects = {}
rice = 10
nori = 10
roe = 10

gameStarted = False

os.chdir(r'E:\DropBox\Dropbox\Elektronika\Programowanie\Python\SushiGoRound\assets')


def map_screen():
    dict_map = dict(res_rice=pyautogui.locateCenterOnScreen('rice.png'),
                    res_nori=pyautogui.locateCenterOnScreen('nori.png'),
                    res_roe=pyautogui.locateCenterOnScreen('roe.png'),
                    phone=pyautogui.locateCenterOnScreen('phone.png'),
                    deliver=pyautogui.locateCenterOnScreen('empty_table.png'))

    # Mapping inital phone menu
    pyautogui.click(dict_map['phone'])
    dict_map['select_rice'] = pyautogui.locateCenterOnScreen('select_rice.png')
    dict_map['select_other'] = pyautogui.locateCenterOnScreen('select_other.png')

    click_on_match('terminate_call.png')

    return dict_map


def click_on_match(pattern):
    coordinates = pyautogui.locateCenterOnScreen(pattern)
    while coordinates is None:
        coordinates = pyautogui.locateCenterOnScreen(pattern)
    pyautogui.click(coordinates)
    pyautogui.moveTo(mouseIdle)


def click_on_match_if_possible(pattern):
    coordinates = pyautogui.locateCenterOnScreen(pattern)
    if coordinates is not None:
        pyautogui.click(coordinates)


def wait_for_match(pattern, timeout=1):
    start = time.time()
    while pyautogui.locateCenterOnScreen(pattern) is None:
        if start + timeout < time.time():
            return False
    return True


def check_if_match(pattern):
    coordinates = pyautogui.locateCenterOnScreen(pattern)
    if coordinates is not None:
        return coordinates
    else:
        return None


def order(resource, objects):
    global rice, nori, roe
    pyautogui.click(objects['phone'])
    if resource == 'rice':
        pyautogui.click(objects['select_rice'])
        coordinates = check_if_match('rice_order.png')
        if coordinates is not None:
            pyautogui.click(coordinates)
            rice += 10
        else:
            click_on_match('terminate_call.png')
            return None
    elif resource == 'nori':
        pyautogui.click(objects['select_other'])
        coordinates = check_if_match('nori_order.png')
        if coordinates is not None:
            pyautogui.click(coordinates)
            nori += 10
        else:
            click_on_match('terminate_call.png')
            return None
    elif resource == 'roe':
        pyautogui.click(objects['select_other'])
        coordinates = check_if_match('roe_order.png')
        if coordinates is not None:
            pyautogui.click(coordinates)
            roe += 10
        else:
            click_on_match('terminate_call.png')
            return None
    click_on_match('free_order.png')


def resupply(objects):
    global rice, nori, roe
    if rice <= 5:
        order('rice', objects)
    if nori <= 5:
        order('nori', objects)
    if roe <= 5:
        order('roe', objects)


def start_game():
    click_on_match('play.png')
    click_on_match('continue.png')
    click_on_match('skip.png')
    click_on_match('continue.png')


def prepare_onigiri(objects):
    global rice, nori
    if rice < 2 or nori < 1:
        return False
    if not wait_for_match('empty_table.png'):
        return False
    pyautogui.doubleClick(objects['res_rice'])
    rice -= 2
    pyautogui.click(objects['res_nori'])
    nori -= 1
    pyautogui.click(objects['deliver'])
    return True


def prepare_california_roll(objects):
    global rice, nori, roe
    if rice < 1 or nori < 1 or roe < 1:
        return False
    if not wait_for_match('empty_table.png'):
        return False
    pyautogui.click(objects['res_rice'])
    rice -= 1
    pyautogui.click(objects['res_nori'])
    nori -= 1
    pyautogui.click(objects['res_roe'])
    roe -= 1
    pyautogui.click(objects['deliver'])
    return True


def prepare_gunkan_maki(objects):
    global rice, nori, roe
    if rice < 1 or nori < 1 or roe < 2:
        return False
    if not wait_for_match('empty_table.png'):
        return False
    pyautogui.click(objects['res_rice'])
    rice -= 1
    pyautogui.click(objects['res_nori'])
    nori -= 1
    pyautogui.doubleClick(objects['res_roe'])
    roe -= 2
    pyautogui.click(objects['deliver'])
    return True


def empty_plates(seconds):
    start = time.time()
    while start + seconds > time.time():
        click_on_match_if_possible('plate1.png')
        click_on_match_if_possible('plate2.png')
        click_on_match_if_possible('plate3.png')
        click_on_match_if_possible('plate4.png')
        click_on_match_if_possible('plate5.png')
        click_on_match_if_possible('plate6.png')


if not gameStarted:
    start_game()
    gameStarted = True
    basicObjects = map_screen()

while True:
    prepare_onigiri(basicObjects)
    prepare_california_roll(basicObjects)
    prepare_gunkan_maki(basicObjects)
    resupply(basicObjects)
    empty_plates(5)
