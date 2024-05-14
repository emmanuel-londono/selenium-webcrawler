from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os

website = "https://www.satbeams.com/satellites?status=active"
t_body='//*[@id="sat_grid"]/tbody/tr[@class="class_tr"]'


def safe_find_next(element, label):
    try:
        next_elem = element.find(string=label)
        if next_elem:
            next_elem = next_elem.find_next()
            if next_elem:
                return next_elem.text.strip()
        return "N/A"
    except Exception as e:
        print(f"Error finding next element for label '{label}': {e}")
        return "N/A"



try:
    driver = webdriver.Chrome()
    driver.get(website)
    driver.implicitly_wait(5)
    
    tr_body_elements = driver.find_elements(By.XPATH,t_body)
    # Set to store ALL URLs
    hrefs = []
    # Set to store unique URLs
    unique_hrefs = set()

    # Iterate over all tbody_tr elements
    for tr in tr_body_elements:
        try:
            #Check for tag presence
            a_tag = WebDriverWait(tr, 10).until(
                EC.presence_of_element_located((By.XPATH, './/a[@class="link" and contains(@href, "/satellites?norad=")]'))
            )
            href_value = a_tag.get_attribute('href')
            hrefs.append(href_value)
            unique_hrefs.add(href_value)
        except Exception as e:
            print(f"Error finding a tag in tr: {e}")


    print(f"Number of unique hrefs: {len(unique_hrefs)}")   
     # Visit each href
    for href in unique_hrefs:
        try:
            # Navigate to the href
            driver.get(href)
            # Wait for the new page to load completely
            time.sleep(5)
            
            # Extract data from the new page
            # For example, extract the title of the page
            page_title = driver.title
            print(f"Visited {href}, Page title: {page_title}")
            
            individual_sat_details = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="sat_grid1"]/tbody/tr[2]'))
            )


            #Extract the text from the element
            data_text = individual_sat_details.get_attribute('innerHTML')

            #Parse the extracted text
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(data_text, 'html.parser')

            satellite_data = {}

            #Extract relevant data
            satellite_data['Satellite Name'] = soup.find(string="Satellite Name:").find_next().strip()
            #Assign file title
            def find_next_text(element, label):
                next_elem = soup.find(string=label)
                if next_elem:
                    next_elem = next_elem.find_next()
                    if next_elem:
                        return next_elem.strip()
                return "N/A"

            # Extract relevant data
            satellite_data['Satellite Name'] = find_next_text(soup, "Satellite Name:")
            satellite_name = satellite_data['Satellite Name']
            satellite_data['Status'] = find_next_text(soup, "Status:")
            satellite_data['Position'] = find_next_text(soup, "Position:")
            satellite_data['NORAD'] = soup.find(string="NORAD:").find_next('a').string.strip() if soup.find(string="NORAD:") else "N/A"
            satellite_data['Cospar number'] = soup.find(string="Cospar number:").find_next('a').string.strip() if soup.find(string="Cospar number:") else "N/A"
            satellite_data['Operator'] = soup.find(string="Operator:").find_next('a').string.strip() if soup.find(string="Operator:") else "N/A"
            satellite_data['Launch date'] = find_next_text(soup, "Launch date:")
            satellite_data['Launch site'] = soup.find(string="Launch site:").find_next('a').string.strip() if soup.find(string="Launch site:") else "N/A"
            satellite_data['Launch vehicle'] = soup.find(string="Launch vehicle:").find_next('a').string.strip() if soup.find(string="Launch vehicle:") else "N/A"
            satellite_data['Launch mass (kg)'] = find_next_text(soup, "Launch mass (kg):")
            satellite_data['Dry mass (kg)'] = find_next_text(soup, "Dry mass (kg):")
            satellite_data['Manufacturer'] = soup.find(string="Manufacturer:").find_next('a').string.strip() if soup.find(string="Manufacturer:") else "N/A"
            satellite_data['Model (bus)'] = soup.find(string="Model (bus):").find_next('a').string.strip() if soup.find(string="Model (bus):") else "N/A"
            satellite_data['Orbit'] = find_next_text(soup, "Orbit:")
            satellite_data['Expected lifetime'] = find_next_text(soup, "Expected lifetime:")

            #Sanitize Satellite Name
            sanitized_name = "".join(c if c.isalnum() or c in " ._-" else "_" for c in satellite_name)
            # Ensure the output directory exists
            if not os.path.exists(sanitized_name):
                os.makedirs(sanitized_name)
            file_path = os.path.join(sanitized_name, f"{sanitized_name}.txt")
            with open(file_path, 'w') as file:
                for key, value in satellite_data.items():
                    file.write(f'{key}: {value}\n')
            
            # Go back to the initial page
            driver.back()
            # Optional: wait for the initial page to load completely
            time.sleep(5)
            
        except Exception as e:
            print(f"Error visiting href {href}: {e}")    
finally:
    driver.quit()