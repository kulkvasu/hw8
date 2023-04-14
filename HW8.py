# Your name: Vasundhara Kulkarni
# Your student id: kulkvasu
# Your email: kulkvasu@umich.edu
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    final = {}
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('SELECT restaurants.name, categories.category, buildings.building, restaurants.rating FROM restaurants JOIN categories ON restaurants.category_id = categories.id JOIN buildings ON restaurants.building_id = buildings.id')
    data = cur.fetchall()
    for row in data:
        final[row[0]] = {'category':row[1], 'building':row[2], 'rating':row[3]}
    return final

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute("SELECT categories.category, COUNT(*) FROM restaurants INNER JOIN categories ON restaurants.category_id = categories.id GROUP BY categories.category")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    final = {}
    for row in rows:
        final[row[0]] = row[1]
    sorted_dict = dict(sorted(final.items(), key=lambda item: item[1]))

    y = list(sorted_dict.keys())
    x = list(sorted_dict.values())
    plt.barh(y, x)
    plt.xticks(range(1, 5))
    plt.title("Types of Restaurants on South University Ave")
    plt.ylabel("Restaurant Categories")
    plt.xlabel("Number of Restaurants")
    plt.savefig("Types_of_Restaurants_Bar_Chart.png", bbox_inches='tight')
    plt.show()
    
    return final

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    rest = []
    temp = {}
    cur.execute(f'SELECT restaurants.name, restaurants.rating FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id WHERE buildings.building = "{building_num}"')
    rows = cur.fetchall()
    for row in rows:
        temp[row[0]] = row[1]
    temp = dict(sorted(temp.items(), key=lambda item: item[1], reverse=True))
    for key in temp:
        rest.append(key)
    return rest

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    fig = plt.figure(figsize=(8,8))
    rest = []

    cur.execute('SELECT categories.category, AVG(restaurants.rating) FROM restaurants JOIN categories ON categories.id = restaurants.category_id GROUP BY restaurants.category_id')
    catAvg = cur.fetchall()

    bestCat = max(catAvg, key=lambda x: x[1])
    rest.append(bestCat)

    catLab, catRat = zip(*catAvg)
    temp = {}
    for i in range(0,len(catLab)):
        temp[catLab[i]] = catRat[i]
    sorted_temp1 = dict(sorted(temp.items(), key=lambda item: item[1]))
    ax1 = fig.add_subplot(211)
    ax1.barh(list(sorted_temp1.keys()), list(sorted_temp1.values()))
    ax1.set_title("Average Restaurant Ratings by Category")
    ax1.set_xlabel("Ratings")
    ax1.set_ylabel("Categories")
    plt.xticks(range(1, 6))

    buildRat = {}
    cur.execute('SELECT buildings.building, AVG(restaurants.rating) FROM restaurants JOIN buildings ON buildings.id = restaurants.building_id GROUP BY restaurants.building_id')
    for row in cur:
        buildRat[row[0]] = round(row[1], 1)
    sortedBuild = sorted(buildRat.items(), key=lambda x: x[1])
    highestRatedBuilding = sortedBuild[-1]
    rest.append(highestRatedBuilding)

    buildings = [str(building[0]) for building in sortedBuild]
    buildingRatings = [building[1] for building in sortedBuild]
    
    ax2 = fig.add_subplot(212)
    ax2.barh(buildings, buildingRatings)
    ax2.set_title("Average Restaurant Ratings by Building")
    ax2.set_xlabel("Ratings")
    ax2.set_ylabel("Buildings")
    # Avoid Overlap
    fig.tight_layout(pad=0.5)
    fig.savefig('EC.png', bbox_inches='tight')
    plt.figure().clear()
    return rest


#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
