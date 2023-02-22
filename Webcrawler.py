from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json;

def webscrape():
    
    base_url = "https://www.nettiauto.com/vaihtoautot/bensiiniautot?id_gear_type=3&pfrom=2500&pto=9000&id_country[]=73&mileageFrom=0&mileageTo=135000&road_permit=Y&id_acc_air=7&id_acc_cruise_control=20&chargingPowerFrom=&chargingPowerTo=page=4&page={}"
    current_page = 1
    driver = webdriver.Chrome(executable_path="C:/Users/Eemil.Korkka/chromedriver_win32/chromedriver.exe")
    url = base_url.format(current_page)
    driver.get(url)
    soup_source = driver.page_source
    soup = BeautifulSoup(soup_source, "html5lib")
    
    total_pages_num = int(soup.find("span", class_="totPage").text)
    
    while current_page <= total_pages_num:
        
        driver = webdriver.Chrome(executable_path="C:/Users/Eemil.Korkka/chromedriver_win32/chromedriver.exe")
        url = base_url.format(current_page)
        driver.get(url)
        soup_source = driver.page_source
        soup = BeautifulSoup(soup_source, "html5lib")
        
        cars = soup.body.find_all('a', class_="childVifUrl tricky_link")

        current_page += 1
        
        for car in cars:
            
            # Dictionary for the JSON file.
            dictionary = {
                "Merkki": car.string,
                "Malli": car["data-model"],
                "Hinta": car["data-price"],
                "Ajetut kilometrit": car["data-mileage"],
                "Linkki": car["href"]
            }
            
            # Send the data of the cars to a JSON file.
            with open("Data.json", "a") as outfile:
                json.dump(dictionary, outfile)
                outfile.write("," + "\n")
    time.sleep(5)
    driver.quit()
    
    print("Data was successfully sent to JSON file.")
       
webscrape()