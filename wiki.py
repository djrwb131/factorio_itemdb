import bs4
import grequests
import requests
import json
from pathlib import Path

def retrieve_all(force = False):
    if Path("wiki.json").is_file() and not force:
        return True
    
    URL = 'https://wiki.factorio.com'

    #materials_page = requests.get(URL + '/Materials_and_recipes').text
    #mat_soup = bs4.BeautifulSoup(materials_page,'html.parser')

    #item_links = [ x.find('a').get('href') for x in mat_soup.find_all(class_='factorio-icon')]
    item_links = [ '/Kovarex_enrichment_process' ]
    items = dict()

        
    # bulk request

    bulk = ( grequests.get(URL + href) for href in item_links )
    item_links = grequests.imap(bulk, size=20)
    
    # Populate dictionary with item details
    for link in item_links:
        item_soup = bs4.BeautifulSoup(link.text,'html.parser')
        name = item_soup.find('h1').contents[0]
        print("---" + name + "---")
        
        
        text_soup = item_soup.find_all('tbody')
        print("%i tbody tags found" % len(text_soup))
        
        
        
        item_time = 0
        item_count = 0
        item_ingredients = []

        test_rows = []
        # Find the first table that contains recipe information
        for test_table in text_soup:
            test_rows = test_table.find_all(lambda tag: tag.name == 'tr' and 'ecipe' in tag.text)
            if len(test_rows) == 0:
                print("No recipe found for %s" % name)
                print(test_rows)
                items[name]=( 0, 0, ())
                continue
            error = False
            for test_row in test_rows:
                try:
                    error = True
                    row = test_row.parent.find_all('td')[1]
                    item_elements = row.find_all('a')
                    print(row)
                    input()
                    for elem in item_elements:
                        if elem.get('title') == 'Time':
                            item_time = elem.parent.find(class_ = 'factorio-icon-text').contents[0]
                        elif elem.get('title') == name:
                            item_count = elem.parent.find(class_ = 'factorio-icon-text').contents[0]
                        else:
                            ingredient_name = elem.get('title')
                            ingredient_count = elem.parent.find(class_ = 'factorio-icon-text').contents[0]
                            item_ingredients.append( (ingredient_name,ingredient_count) )
                    error = False
                    break
                except AttributeError:
                    #print("Error loading recipe for %s" % name)
                    #print(row)
                    item_ingredients.clear()
                    item_time = 0
                    item_count = 0
            if not error:
                break
                    
        print("Time: " + str(item_time) + " for " + str(item_count))
        for ingredient in item_ingredients:
            print(str(ingredient[1]) + "x " + str(ingredient[0]))
        print("------")
        items[name]= (item_time, item_count, item_ingredients)

    with open("wiki.json","w") as file:
        json.dump(items,file)
