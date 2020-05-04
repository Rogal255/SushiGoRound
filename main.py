# Totally basic code to pass first day in sushi go round
# Script made to learn python
# Only first day of game covered
# 04/05/2020 07:30 Piotr Rogalski

# TODO: Sushi making based on orders rather than upfront randomly

import pyautogui
import os
import time

mouseIdle = (100, 100)
clickDelay = 1
rice = 10
nori = 10
roe = 10

gameStarted = False

os.chdir(r'E:\DropBox\Dropbox\Elektronika\Programowanie\Python\SushiGoRound\assets')


def click_on_match(pattern):
    while True:
        coordinates = pyautogui.locateCenterOnScreen(pattern)
        if coordinates is not None:
            pyautogui.click(coordinates)
            pyautogui.moveTo(mouseIdle)
            break


def click_on_match_if_possible(pattern):
    coordinates = pyautogui.locateCenterOnScreen(pattern)
    if coordinates is not None:
        pyautogui.click(coordinates)


def double_click_on_match(pattern):
    while True:
        coordinates = pyautogui.locateCenterOnScreen(pattern)
        if coordinates is not None:
            pyautogui.click(coordinates)
            pyautogui.click(coordinates)
            pyautogui.moveTo(mouseIdle)
            break


def wait_for_match(pattern):
    while True:
        if pyautogui.locateCenterOnScreen(pattern) is not None:
            break


def check_if_match(pattern):
    if pyautogui.locateCenterOnScreen(pattern) is not None:
        return True
    else:
        return False


def order(resource):
    global rice, nori, roe
    click_on_match('phone.png')
    if resource == 'rice':
        click_on_match('rice_preorder.png')
        if check_if_match('rice_order.png') is True:
            click_on_match('rice_order.png')
            rice += 10
        else:
            click_on_match('terminate_call.png')
            return None
    elif resource == 'nori':
        click_on_match('rest_preorder.png')
        if check_if_match('nori_order.png') is True:
            click_on_match('nori_order.png')
            nori += 10
        else:
            click_on_match('terminate_call.png')
            return None
    elif resource == 'roe':
        click_on_match('rest_preorder.png')
        if check_if_match('roe_order.png') is True:
            click_on_match('roe_order.png')
            roe += 10
        else:
            click_on_match('terminate_call.png')
            return None
    click_on_match('free_order.png')


def start_game():
    click_on_match('play.png')
    click_on_match('continue.png')
    click_on_match('skip.png')
    click_on_match('continue.png')


def prepare_onigiri():
    global rice, nori
    if rice < 2 or nori < 1:
        return
    wait_for_match('empty_table.png')
    double_click_on_match('rice.png')
    rice -= 2
    click_on_match('nori.png')
    nori -= 1
    click_on_match('deliver.png')


def prepare_california_roll():
    global rice, nori, roe
    if rice < 1 or nori < 1 or roe < 1:
        return
    wait_for_match('empty_table.png')
    click_on_match('rice.png')
    rice -= 1
    click_on_match('nori.png')
    nori -= 1
    click_on_match('roe.png')
    roe -= 1
    click_on_match('deliver.png')


def prepare_gunkan_maki():
    global rice, nori, roe
    if rice < 1 or nori < 1 or roe < 2:
        return
    wait_for_match('empty_table.png')
    click_on_match('rice.png')
    rice -= 1
    click_on_match('nori.png')
    nori -= 1
    double_click_on_match('roe.png')
    roe -= 2
    click_on_match('deliver.png')


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

while True:
    prepare_onigiri()
    prepare_california_roll()
    prepare_gunkan_maki()
    empty_plates(5)
    if rice <= 5:
        order('rice')
    if nori <= 5:
        order('nori')
    if roe <= 5:
        order('roe')
