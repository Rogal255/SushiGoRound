# Totally basic code to play sushi go round
# Script made to learn python
# First three days of game covered
# 11/05/2020 11:00 Piotr Rogalski

# TODO: Investigate bug when game adds less resources than delcared 10 or 5 (for example 8 instead of 10)
# TODO: Map plates position on the 1st day

import pyautogui
import os
import time

os.chdir(r'E:\DropBox\Dropbox\Elektronika\Programowanie\Python\SushiGoRound\assets')
mouseIdle = (100, 250)


class Meal:
    meals_list = []

    def __init__(self, name, rice, nori, roe, salmon, shrimp, unagi, file):
        self.name = name
        self.rice = rice
        self.nori = nori
        self.roe = roe
        self.salmon = salmon
        self.shrimp = shrimp
        self.unagi = unagi
        self.file = file
        Meal.meals_list.append(self)

    def serve_meals(self):
        back_log = self.__check_order_bubbles() - self.__check_meals_on_belt()
        if back_log < 0:
            back_log = 0
        for i in range(back_log):
            self.prepare()

    def prepare(self):
        if self.__check_resources():
            ScreenObject.wait_for_match('empty_table.png')
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

    def __check_resources(self):
        if resource_rice.quantity_property < self.rice:
            return False
        elif resource_nori.quantity_property < self.nori:
            return False
        elif resource_roe.quantity_property < self.roe:
            return False
        elif resource_salmon.quantity_property < self.salmon:
            return False
        elif resource_shrimp.quantity_property < self.shrimp:
            return False
        elif resource_unagi.quantity_property < self.unagi:
            return False
        else:
            return True

    def __check_order_bubbles(self):
        path = os.path.join(os.getcwd(), 'order_bubbles', self.file.format('_bubble') + '.png')
        return len(list(pyautogui.locateAllOnScreen(path, region=screen.coordinates)))

    def __check_meals_on_belt(self):
        path = os.path.join(os.getcwd(), 'meals_belt', self.file.format('_on_belt') + '.png')
        return len(list(pyautogui.locateAllOnScreen(path, region=screen.coordinates)))

    @staticmethod
    def clean_plates():
        for plate in Meal.meals_list:
            path = os.path.join(os.getcwd(), 'plates', plate.file.format('_plate.png'))
            ScreenObject.click_on_match_if_possible(path)


class Resource:
    resources_list = []

    def __init__(self, name, initial_quantity, minimum, coordinates):
        self.name = name
        self.__quantity = initial_quantity
        self.minimum = minimum
        self.coordinates = coordinates
        self.last_ordered = time.time()
        self.is_order_added = True
        Resource.resources_list.append(self)

    def put_on_table(self):
        pyautogui.click(self.coordinates)
        self.__quantity -= 1

    @staticmethod
    def warehouse_keeper():
        for resource_class in Resource.resources_list:
            resource_class.__order()
            resource_class.__update_warehouse()

    def __order(self):
        if self.__quantity < self.minimum and self.is_order_added:
            phone.click()
            if self.name == 'rice':
                phone_select_rice.click()
            else:
                phone_select_other.click()
            coordinates_order = ScreenObject.check_if_match('{}_order.png'.format(self.name))
            if coordinates_order is not False:
                pyautogui.click(coordinates_order)
                ScreenObject.click_on_match('free_order.png')
                self.last_ordered = time.time()
                self.is_order_added = False
            else:
                ScreenObject.click_on_match('terminate_call.png')

    def __update_warehouse(self):
        if self.is_order_added:
            return
        else:
            if self.last_ordered + 5 < time.time():
                self.__add()

    def __add(self):
        if self.name == 'rice' or self.name == 'nori' or self.name == 'roe':
            add_to_quantity = 10
        else:
            add_to_quantity = 5
        self.__quantity += add_to_quantity
        self.is_order_added = True

    @property
    def quantity_property(self):
        return self.__quantity

    @quantity_property.setter
    def quantity_property(self, newQuantity):
        self.__quantity = newQuantity


class ScreenObject:
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def click(self):
        pyautogui.click(self.coordinates)
        pyautogui.moveTo(mouseIdle)

    @staticmethod
    def click_on_match(pattern):
        start = time.time()
        coordinates = ScreenObject.check_if_match(pattern)
        while coordinates is False:
            coordinates = ScreenObject.check_if_match(pattern)
        pyautogui.click(coordinates)
        pyautogui.moveTo(mouseIdle)

    @staticmethod
    def click_on_match_if_possible(pattern):
        coordinates = ScreenObject.check_if_match(pattern)
        if coordinates is not False:
            pyautogui.click(coordinates)

    @staticmethod
    def check_if_match(pattern):
        coordinates = pyautogui.locateCenterOnScreen(pattern, region=screen.coordinates)
        if coordinates is not None:
            return coordinates
        else:
            return False

    @staticmethod
    def wait_for_match(pattern):
        i = 1
        while ScreenObject.check_if_match(pattern) is False:
            Meal.clean_plates()


# This function checks if game day has finished and starts new day
def check_next_level():
    if ScreenObject.check_if_match('win.png') is False:
        return
    start = time.time()
    while True:
        if start + 15 <= time.time():
            ScreenObject.click_on_match('continue.png')
            ScreenObject.click_on_match('continue.png')
            resource_rice.quantity_property = 10
            resource_nori.quantity_property = 10
            resource_roe.quantity_property = 10
            resource_salmon.quantity_property = 5
            resource_shrimp.quantity_property = 5
            resource_unagi.quantity_property = 5
            return


# Determining game screen area and creating ScreenObject class instance
top = pyautogui.locateOnScreen('top.png')
bottom = pyautogui.locateOnScreen('bottom.png')
screen = ScreenObject((bottom[0], top[1], bottom[0] + bottom[2], bottom[1] + bottom[3]))

# Starting the game
ScreenObject.click_on_match('play.png')
ScreenObject.click_on_match('continue.png')
ScreenObject.click_on_match('skip.png')
ScreenObject.click_on_match('continue.png')

# Resource instances
resource_rice = Resource('rice', 10, 7, ScreenObject.check_if_match('rice.png'))
resource_nori = Resource('nori', 10, 7, ScreenObject.check_if_match('nori.png'))
resource_roe = Resource('roe', 10, 7, ScreenObject.check_if_match('roe.png'))
resource_salmon = Resource('salmon', 5, 5, ScreenObject.check_if_match('salmon.png'))
resource_shrimp = Resource('shrimp', 5, 5, ScreenObject.check_if_match('shrimp.png'))
resource_unagi = Resource('unagi', 5, 5, ScreenObject.check_if_match('unagi.png'))

# ScreenObject instances
deliver = ScreenObject(ScreenObject.check_if_match('empty_table.png'))
phone = ScreenObject(ScreenObject.check_if_match('phone.png'))
phone.click()
phone_select_rice = ScreenObject(ScreenObject.check_if_match('select_rice.png'))
phone_select_other = ScreenObject(ScreenObject.check_if_match('select_other.png'))
ScreenObject.click_on_match('terminate_call.png')

# Meal instances
meal_onigiri = Meal('Onigiri', 2, 1, 0, 0, 0, 0, 'onigiri{}')
meal_california_roll = Meal('California Roll', 1, 1, 1, 0, 0, 0, 'california_roll{}')
meal_gunkan_maki = Meal('Gunkan Maki', 1, 1, 2, 0, 0, 0, 'gunkan_maki{}')
meal_salmon_roll = Meal('Salmon Roll', 1, 1, 0, 2, 0, 0, 'salmon_roll{}')
meal_shrimp_sushi = Meal('Shrimp Sushi', 1, 1, 0, 0, 2, 0, 'shrimp_sushi{}')
meal_unagi_roll = Meal('Unagi Roll', 1, 1, 0, 0, 0, 2, 'unagi_roll{}')
meal_dragon_roll = Meal('Dragon Roll', 2, 1, 1, 0, 0, 2, 'dragon_roll{}')
meal_combo_sushi = Meal('Combo Sushi', 2, 1, 1, 1, 1, 1, 'combo_sushi{}')

while True:
    Resource.warehouse_keeper()
    for meal in Meal.meals_list:
        meal.serve_meals()
    Meal.clean_plates()
    check_next_level()
