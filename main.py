from selenium import webdriver
website = "http://localhost:5555/"
driver_path = 'C:/Users/emman/chrome-win64'
driver = webdriver.Chrome(path)
driver.get(website)
result = requests.get(website)

