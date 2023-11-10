from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import os

websites = ["http://localhost:5555/","https://expressjs.com/en/5x/api.html#req", "https://nvd.nist.gov/"]
driver = webdriver.Chrome()
driver.get(websites[0])
driver.implicitly_wait(0.5)
# "//input[@value='f']"
cveList = driver.find_elements(By.XPATH, "//ul[@id='latestVulns']")
tables = driver.find_elements(By.XPATH,"//li[@class='_model_1xigg_60']")
titles = []

for element in tables:
    if(element.find_element(By.XPATH, "./div[1]").text == "aor" or "site"):
        pass
    titles.append(element.find_element(By.XPATH, "./div[1]").text)
driver.quit()
#   context.append(element.find_element(By.XPATH, "/#text")).text
#   published.append(element.find_element(By.XPATH, "/strong[2]")).text

standardEnpoints = []
path = 'path'
router = 'router'
standardRouter = 'standardRouter'

for title in titles :
    standardEnpoints.append( { path: f"/{title}", router: standardRouter })
print(standardEnpoints)

# df = pd.DataFrame({'title':titles})
# df.to_csv('')
# print(df)

# base_directory = ""

# for folder_name in titles:
#     #Create new folder name
#     folder_path = os.path.join(base_directory, folder_name)
#     os.makedirs(folder_path)
#     with open(os.path.join(folder_path,f"{folder_name}.router.ts"),'w'):
#         pass
