from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

base_url = "https://www.nettiauto.com/vaihtoautot/dieselautot?id_vehicle_type=1&id_gear_type=2&id_country[]=73&show_search=1&chargingPowerFrom=&chargingPowerTo=&page={}"

def get_soup(url):
    driver = webdriver.Chrome()
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html5lib")
    driver.quit()
    return soup

current_page = 1
url = base_url.format(current_page)
soup = get_soup(url) 
total_pages_num = int(soup.find("span", class_="totPage").text)

while current_page <= total_pages_num:
    
    soup = get_soup(url)
    
    car_listings = soup.find_all("div", class_="listingVifUrl tricky_link_listing listing_nl odd")
    
    current_page += 1
    
    for car in car_listings:
        
        car_brand = car.find("a", class_="childVifUrl tricky_link").get("data-make")
        car_model = car.find("a", class_="childVifUrl tricky_link").get("data-model")
        car_price = car.find("div", class_="main_price")
        car_link = car.find("a", class_="childVifUrl tricky_link").get("href")
        car_image = car.find('div', class_="listing_thumb").find('img')["data-src"]
        
        # Dictionary for JSON file
        dictionary = {
            "Merkki: ": car_brand,
            "Malli: ": car_model,
            "Hinta: ": car_price.text,
            "Linkki: ": car_link,
            "Kuva: ": car_image          
        }
        
        with open("Autot.json", "a") as outfile:
            json.dump(dictionary, outfile, indent=4)
            outfile.write("," + "\n")
        
        # Update url
        current_page += 1
        url = base_url.format(current_page)
        
    time.sleep(5)   
