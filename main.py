from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
websites = ["http://localhost:5555/","https://expressjs.com/en/5x/api.html#req"]
browser = webdriver.Chrome(options=chrome_options)
browser.get(websites[0])
