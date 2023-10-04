from selenium import webdriver
from dotenv import load_dotenv

load_dotenv()
WEBDRIVER_FILEPATH = os.getenv('WEBDRIVER_FILEPATH')
website = "http://localhost:5555/"

driver = webdriver.Chrome(WEBDRIVER_FILEPATH)
driver.get(website)
result = requests.get(website)

