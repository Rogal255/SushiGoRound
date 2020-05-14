# Totally basic code to play sushi go round
# Script made to learn python
# 14/05/2020 08:00 Piotr Rogalski

# TODO: Investigate bug when game adds less resources than delcared 10 or 5 (for example 8 instead of 10)
# TODO: Prepare 2 meals for the customer seating further away

import pyautogui
import os
import time
import sys

os.chdir('assets')
mouseIdle = (100, 250)


class Meal:
    """
    This class represents Meal object. Instances are created at main function before program main loop. Each instance is
    a representation of one meal available in the game.
    """
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
        """This method finds out how many of certain meals have to be created and calls prepare method accordingly"""
        back_log = self.__check_order_bubbles() - self.__check_meals_on_belt()
        if back_log < 0:
            back_log = 0
        for i in range(back_log):
            self.prepare()

    def prepare(self):
        """
        This method checks if available resources are enough to prepare meal by calling __check_resources method and if
        True - prepares one meal.
        """
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
        """This method checks if available resources are enough to prepare given meal"""
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
        """This method checks number of orders of certain meal"""
        path = os.path.join(os.getcwd(), 'order_bubbles', self.file.format('_bubble') + '.png')
        return len(list(pyautogui.locateAllOnScreen(path, region=screen.coordinates)))

    def __check_meals_on_belt(self):
        """This method checks how many certain meals are on belt waiting to be taken by customers"""
        path = os.path.join(os.getcwd(), 'meals_belt', self.file.format('_on_belt') + '.png')
        return len(list(pyautogui.locateAllOnScreen(path, region=screen.coordinates)))


class Resource:
    """
    This class represents resources available in the game. Each instance (which by the way is declared in the main body
    before main program loop) represents certain resource.
    """
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
        """
        This method puts certain resource on table. Typically is called from Meal class. Coordinates of resource are
        mapped when game starts
        """
        pyautogui.click(self.coordinates)
        self.__quantity -= 1

    @staticmethod
    def warehouse_keeper():
        """
        This static method calls __order and __update_warehouse methods. Just binds them together making it easier
        to manage resources form main body program.
        """
        for resource_class in Resource.resources_list:
            resource_class.__order()
            resource_class.__update_warehouse()

    def __order(self):
        """
        This method orders new resources if certain resource is below minimum.
        """
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
        """
        This method updates number (by calling __add method) of resources in program memory when certain time passed from order.
        """
        if self.is_order_added:
            return
        else:
            if self.last_ordered + 5 < time.time():
                self.__add()

    def __add(self):
        """
        This method updates number of resoruces based on type of resource and is called only form __update_warehouse method
        """
        if self.name == 'rice' or self.name == 'nori' or self.name == 'roe':
            add_to_quantity = 10
        else:
            add_to_quantity = 5
        self.__quantity += add_to_quantity
        self.is_order_added = True

    @property
    def quantity_property(self):
        """
        Property of private __quantity variable.
        """
        return self.__quantity

    @quantity_property.setter
    def quantity_property(self, newQuantity):
        """
        This setter allows to set new value to private __quantity variable.
        """
        self.__quantity = newQuantity


class ScreenObject:
    """
    This class represents variety of objects on the screen.
    """
    plates_coordinates = []

    def __init__(self, coordinates):
        self.coordinates = coordinates

    def click(self):
        """
        This method clicks on instance coordinates. Coordinates are mapped during instance initialization.
        """
        pyautogui.click(self.coordinates)
        pyautogui.moveTo(mouseIdle)

    @classmethod
    def map_plates(cls):
        """This method maps plates left by customers and takes them away"""
        if len(cls.plates_coordinates) == 6:
            return
        for plate in Meal.meals_list:
            path = os.path.join('plates', plate.file.format('_plate.png'))
            coordinates = ScreenObject.click_on_match_if_possible(path)
            if coordinates is not False:
                if not cls.plates_coordinates:
                    cls.plates_coordinates.append(coordinates)
                else:
                    misses = 0
                    for coords in cls.plates_coordinates:
                        if (coords.x < coordinates.x + 30) and (coords.x > coordinates.x - 30):
                            break
                        else:
                            misses += 1
                    if misses == len(cls.plates_coordinates):
                        cls.plates_coordinates.append(coordinates)

    @classmethod
    def clean_mapped_plates(cls):
        for coordinates in cls.plates_coordinates:
            pyautogui.click(coordinates)

    @staticmethod
    def click_on_match(pattern):
        """
        This method clicks on object from .png file. When match is not possible - method waits until it is possible.
        """
        start = time.time()
        coordinates = ScreenObject.check_if_match(pattern)
        while coordinates is False:
            coordinates = ScreenObject.check_if_match(pattern)
        pyautogui.click(coordinates)
        pyautogui.moveTo(mouseIdle)

    @staticmethod
    def click_on_match_if_possible(pattern):
        """
        This method clicks on object from .png file when possible. If not - returns.
        """
        coordinates = ScreenObject.check_if_match(pattern)
        if coordinates is not False:
            pyautogui.click(coordinates)
            return coordinates
        else:
            return False

    @staticmethod
    def check_if_match(pattern):
        """
        This method checks if match with an object form .png file is possible. If not - returns False.
        """
        coordinates = pyautogui.locateCenterOnScreen(pattern, region=screen.coordinates)
        if coordinates is not None:
            return coordinates
        else:
            return False

    @staticmethod
    def wait_for_match(pattern):
        """
        This method waits until match with an object from .png file is possible. Calls clean_plates method from Meal class
        during waiting period. This plates method will be rewritten.
        """
        while ScreenObject.check_if_match(pattern) is False:
            ScreenObject.clean_mapped_plates()
            ScreenObject.map_plates()


class Level:
    """
    This class keeps track of current level being played and initialises new level.
    """
    current_level = 1

    @classmethod
    def level_init(cls):
        """
        This method initialises warehause values when passing to new level. Also initislises meal instances - there is
        no point in checking all the meals during couple of first levels so as game progresses new meal instances are
        added.
        """
        resource_rice.quantity_property = 10
        resource_nori.quantity_property = 10
        resource_roe.quantity_property = 10
        resource_salmon.quantity_property = 5
        resource_shrimp.quantity_property = 5
        resource_unagi.quantity_property = 5

        # Meal instances init
        if cls.current_level == 1:
            meal_onigiri = Meal('Onigiri', 2, 1, 0, 0, 0, 0, 'onigiri{}')
            meal_california_roll = Meal('California Roll', 1, 1, 1, 0, 0, 0, 'california_roll{}')
            meal_gunkan_maki = Meal('Gunkan Maki', 1, 1, 2, 0, 0, 0, 'gunkan_maki{}')
        elif cls.current_level == 2:
            meal_salmon_roll = Meal('Salmon Roll', 1, 1, 0, 2, 0, 0, 'salmon_roll{}')
        elif cls.current_level == 3:
            meal_shrimp_sushi = Meal('Shrimp Sushi', 1, 1, 0, 0, 2, 0, 'shrimp_sushi{}')
        elif cls.current_level == 4:
            meal_unagi_roll = Meal('Unagi Roll', 1, 1, 0, 0, 0, 2, 'unagi_roll{}')
        elif cls.current_level == 5:
            meal_dragon_roll = Meal('Dragon Roll', 2, 1, 1, 0, 0, 2, 'dragon_roll{}')
        elif cls.current_level == 6:
            meal_combo_sushi = Meal('Combo Sushi', 2, 1, 1, 1, 1, 1, 'combo_sushi{}')
        for x in Meal.meals_list:
            print(x.name)
        print("-"*30)

    @classmethod
    def check_next_level(cls):
        """
        This function checks if game day has finished and starts new day.
        """
        if ScreenObject.check_if_match('win.png') is False:
            return
        else:
            start = time.time()
            while True:
                if start + 15 <= time.time():
                    ScreenObject.click_on_match('continue.png')
                    ScreenObject.click_on_match('continue.png')
                    cls.current_level += 1
                    if cls.current_level <= 7:
                        cls.level_init()
                    else:
                        print("The game has ended. Congratulations!")
                        sys.exit()
                    return


# Determining game screen area and creating ScreenObject class instance
top = pyautogui.locateOnScreen('top.png')
bottom = pyautogui.locateOnScreen('bottom.png')
try:
    screen = ScreenObject((bottom[0], top[1], bottom[0] + bottom[2], bottom[1] + bottom[3]))
except Exception:
    print("Whole game area with \"play\" button must be in view. Program has stopped.")
    sys.exit(1)

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

Level.level_init()

while True:
    Resource.warehouse_keeper()
    ScreenObject.clean_mapped_plates()
    for meal in Meal.meals_list:
        meal.serve_meals()
    ScreenObject.clean_mapped_plates()
    ScreenObject.map_plates()
    Level.check_next_level()
