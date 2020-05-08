# Totally basic code to pass first day in sushi go round
# Script made to learn python
# Only first two day of game covered
# 08/05/2020 08:00 Piotr Rogalski

# TODO: Day 3
# TODO: Investigate bug when game adds less resources than delcared 10 or 5 (for example 8 instead of 10)

import pyautogui
import os
import time

os.chdir(r'E:\DropBox\Dropbox\Elektronika\Programowanie\Python\SushiGoRound\assets')
mouseIdle = (100, 250)


class Meal:
    def __init__(self, name, rice, nori, roe, salmon, shrimp, unagi, customerOrderImg):
        self.name = name
        self.rice = rice
        self.nori = nori
        self.roe = roe
        self.salmon = salmon
        self.shrimp = shrimp
        self.unagi = unagi
        self.customerOrderImg = customerOrderImg

    def check_resources(self):
        if resource_rice.value < self.rice:
            return False
        elif resource_nori.value < self.nori:
            return False
        elif resource_roe.value < self.roe:
            return False
        elif resource_salmon.value < self.salmon:
            return False
        elif resource_shrimp.value < self.shrimp:
            return False
        elif resource_unagi.value < self.unagi:
            return False
        else:
            return True

    def prepare(self):
        if self.check_resources():
            wait_for_match('empty_table.png')
            for i in range(self.rice):
                resource_rice.put_on_table()
            for i in range(self.nori):
                resource_nori.put_on_table()
            for i in range(self.roe):
                resource_roe.put_on_table()
            for i in range(self.salmon):
                resource_salmon.put_on_table()
            for i in range(self.shrimp):
                resource_shrimp.put_on_table()
            for i in range(self.unagi):
                resource_unagi.put_on_table()
            deliver.click()


class Resource:
    def __init__(self, name, initial_value, minimum, coordinates):
        self.name = name
        self.value = initial_value
        self.minimum = minimum
        self.coordinates = coordinates
        self.last_ordered = time.time()
        self.is_order_added = True

    def put_on_table(self):
        pyautogui.click(self.coordinates)
        self.value -= 1

    def add(self):
        if self.name == 'rice' or self.name == 'nori' or self.name == 'roe':
            quantity = 10
        else:
            quantity = 5
        self.value += quantity
        print("Adding {} to {}, now: {}".format(quantity, self.name, self.value))
        self.is_order_added = True

    def order(self):
        if self.value < self.minimum and self.is_order_added:
            phone.click()
            if self.name == 'rice':
                phone_select_rice.click()
            else:
                phone_select_other.click()
            coordinates_order = check_if_match('{}_order.png'.format(self.name))
            if coordinates_order is not False:
                pyautogui.click(coordinates_order)
                click_on_match('free_order.png')
                self.last_ordered = time.time()
                self.is_order_added = False
            else:
                click_on_match('terminate_call.png')

    def add_to_warehouse(self):
        if self.is_order_added:
            return
        else:
            if self.last_ordered + 5 < time.time():
                self.add()

    def check(self):
        return self.value


class ScreenObject:
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def click(self):
        pyautogui.click(self.coordinates)
        pyautogui.moveTo(mouseIdle)


# This function checks if game day has finished and starts new day
def check_next_level():
    if check_if_match('win.png') is False:
        return
    start = time.time()
    while True:
        if start + 15 <= time.time():
            click_on_match('continue.png')
            click_on_match('continue.png')
            resource_rice.value = 10
            resource_nori.value = 10
            resource_roe.value = 10
            resource_salmon.value = 5
            resource_shrimp.value = 5
            resource_unagi.value = 5


def click_on_match(pattern, timeout=1):
    start = time.time()
    coordinates = check_if_match(pattern)
    while coordinates is False:
        coordinates = check_if_match(pattern)
        if start + timeout < time.time():
            return
    pyautogui.click(coordinates)
    pyautogui.moveTo(mouseIdle)


def click_on_match_if_possible(pattern):
    coordinates = check_if_match(pattern)
    if coordinates is not False:
        pyautogui.click(coordinates)


def wait_for_match(pattern, timeout=1):
    start = time.time()
    while check_if_match(pattern) is False:
        if start + timeout < time.time():
            return


def check_if_match(pattern):
    coordinates = pyautogui.locateCenterOnScreen(pattern, region=screen.coordinates)
    if coordinates is not None:
        return coordinates
    else:
        return False


def warehouse_keeper(resource_class_list):
    for resource_class in resource_class_list:
        resource_class.order()
        resource_class.add_to_warehouse()


def check_orders_and_prepare_meals(meal):
    orders = len(list(pyautogui.locateAllOnScreen(meal + '_customer.png')))
    prepared = len(list(pyautogui.locateAllOnScreen(meal + '_on_belt.png')))
    to_prepare = orders - prepared
    if to_prepare < 0:
        to_prepare = 0
    for i in range(to_prepare):
        if meal == 'onigiri':
            meal_onigiri.prepare()
        elif meal == 'california_roll':
            meal_california_roll.prepare()
        elif meal == 'gunkan_maki':
            meal_gunkan_maki.prepare()
        elif meal == 'salmon_roll':
            meal_salmon_roll.prepare()
        elif meal == 'shrimp_sushi':
            meal_shrimp_sushi.prepare()


def empty_plates():
    for i in range(1, 8):
        click_on_match_if_possible('plate{}.png'.format(i))


# Determining game screen area and creating ScreenObject class instance
top = pyautogui.locateOnScreen('top.png')
bottom = pyautogui.locateOnScreen('bottom.png')
screen = ScreenObject((bottom[0], top[1], bottom[0] + bottom[2], bottom[1] + bottom[3]))

# Starting the game
click_on_match('play.png')
click_on_match('continue.png')
click_on_match('skip.png')
click_on_match('continue.png')

# Resource instances
resource_rice = Resource('rice', 10, 7, pyautogui.locateCenterOnScreen('rice.png', region=screen.coordinates))
resource_nori = Resource('nori', 10, 7, pyautogui.locateCenterOnScreen('nori.png', region=screen.coordinates))
resource_roe = Resource('roe', 10, 7, pyautogui.locateCenterOnScreen('roe.png', region=screen.coordinates))
resource_salmon = Resource('salmon', 5, 5, pyautogui.locateCenterOnScreen('salmon.png', region=screen.coordinates))
resource_shrimp = Resource('shrimp', 5, 5, pyautogui.locateCenterOnScreen('shrimp.png', region=screen.coordinates))
resource_unagi = Resource('unagi', 5, 5, pyautogui.locateCenterOnScreen('unagi.png', region=screen.coordinates))
# Resource instances list
resources = [resource_rice, resource_nori, resource_roe, resource_salmon, resource_shrimp, resource_unagi]

# ScreenObject instances
deliver = ScreenObject(pyautogui.locateCenterOnScreen('empty_table.png', region=screen.coordinates))
phone = ScreenObject(pyautogui.locateCenterOnScreen('phone.png', region=screen.coordinates))
phone.click()
phone_select_rice = ScreenObject(pyautogui.locateCenterOnScreen('select_rice.png', region=screen.coordinates))
phone_select_other = ScreenObject(pyautogui.locateCenterOnScreen('select_other.png', region=screen.coordinates))
click_on_match('terminate_call.png')

# Meal instances
meal_onigiri = Meal('Onigiri', 2, 1, 0, 0, 0, 0, 'onigiri_customer.png')
meal_california_roll = Meal('California Roll', 1, 1, 1, 0, 0, 0, 'california_roll_customer.png')
meal_gunkan_maki = Meal('Gunkan Maki', 1, 1, 2, 0, 0, 0, 'gunkan_maki_customer.png')
meal_salmon_roll = Meal('Salmon Roll', 1, 1, 0, 2, 0, 0, 'salmon_roll_customer.png')
meal_shrimp_sushi = Meal('Shrimp Sushi', 1, 1, 0, 0, 2, 0, 'shrimp_sushi_customer.png')
# Meal instances list
meals = [meal_onigiri, meal_california_roll, meal_gunkan_maki, meal_salmon_roll, meal_shrimp_sushi]

while True:
    warehouse_keeper(resources)
    empty_plates()
    check_orders_and_prepare_meals('onigiri')
    check_orders_and_prepare_meals('california_roll')
    empty_plates()
    check_orders_and_prepare_meals('gunkan_maki')
    check_orders_and_prepare_meals('salmon_roll')
    empty_plates()
    check_next_level()
