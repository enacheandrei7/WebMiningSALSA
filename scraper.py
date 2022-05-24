# import os
# import wget
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait


# driver = webdriver.Chrome('C:/Users/Enachele/Desktop/Master An 1/S2/DMDW/Proiect/Code/SALSA/chromedriver.exe')
# driver.get('https://www.tripadvisor.com/Restaurants-g294458-Bucharest.html')

from bs4 import BeautifulSoup
import requests

site = "https://www.restaurante-bucuresti.com/"

try:
    source = requests.get(site)
    # source = requests.get('https://ialoc.ro/restaurante-bucuresti')
    # source = requests.get('https://www.restocracy.ro/')
    
    
    source.raise_for_status()

    soup = BeautifulSoup(source.text, 'html.parser')

    # restaurante-bucuresti.com
    restaurants = soup.find('div', class_ = "content").find_all('div', class_="companyBox")

    # ialoc.ro
    # restaurants = soup.find('div', class_ = "hotel-list-cn clearfix").find_all('div', class_="list-item venue-link")
    
    for restaurant in restaurants:

        link_to_restaurant = restaurant.find('div', class_="companyBox_title").a.get("href")

        new_src = requests.get(site + link_to_restaurant)
        new_soup = BeautifulSoup(new_src.text, 'html.parser')

        contact_details = new_soup.find('div', class_="row_details").find_all('p')

        restaurant_link = ""
        for p in contact_details:
            if p.a and ".ro" in p.a.get("href"):
                print(p.a.get("href").strip())
                break

    
except Exception as e:
    print(e)