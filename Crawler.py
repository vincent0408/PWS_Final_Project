from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
import os

# Disable web_manager.Chrome from printing useless logs
# Hacky workaround as log_level=0 is not implemented properly by the author of webdriver_manager
os.environ['WDM_LOG_LEVEL'] = '0'  

# Initialize fake user agent object for crawler
ua = UserAgent()

# Add options to prevent useless logs, fake user agent
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent=" + ua.random)
chrome_options.add_argument("--start-maximized");
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(ChromeDriverManager(print_first_line=False).install(), options=chrome_options)

# Change personal info to your own judge.ccClub.io account
username = ''
password = ''

url = 'https://judge.ccclub.io/contest'

# Modify save file location to sth like 'C:/Users/jiaojiaozhe/Desktop/'
SAVE_FILE_PATH = ''

# List of contest names to crawl
hw = ['PWS HW1', 'ccClub Homework 1']

# Login to judge.ccClub.io/contest
def login():
    driver.get(url)

    # Bypass browser detection
    try:
        driver.switch_to.alert.dismiss();
        login_button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn-menu')))
        login_button.click()
    except:
        login_button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.btn-menu')))
        login_button.click()
        
        
    username_box = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.ivu-input-large[placeholder = "Username"]')))
    username_box.send_keys(username)
    password_box = driver.find_element_by_css_selector('.ivu-input-large[placeholder = "Password"]')
    password_box.send_keys(password)
    confirm_login_button = driver.find_element_by_css_selector('.ivu-btn-long')
    confirm_login_button.click()

# Show submission page 1 according to the hw_name given
def loadSubmissionPage(hw_name):
    press_hw = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, hw_name)))
    press_hw.click()

    # Necessary for PWS HWX
    try:
        find_hw_pw = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'input[placeholder = "contest password"]')))
        find_hw_pw.send_keys('pws')    
        enter_hw_pw = driver.find_element_by_css_selector('.ivu-btn-info')
        enter_hw_pw.click()
    except:
        pass
    submissions_tab = driver.find_element_by_css_selector('.ivu-icon-navicon-round')
    submissions_tab.click()

            
# Get submission table data, 12*8
def getSubmission(hw_name):

    # Get table and rows
    submission_table = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.ivu-table-tbody')))
    tr_collection = submission_table.find_elements_by_css_selector('tr')
    
    data = ''

    # Write data to csv, 1 table at a time
    # Traditional way over pandas read_html due to the tbody tag in original HTML structure causing slower loading time if using pandas
    for row in tr_collection:

        # Improve concatenate speed using join instead of +=
        cell_data = [cell.text for cell in row.find_elements_by_css_selector('td')]
        cell_data[3] = '{} {}'.format(hw_name, cell_data[3])
        data += (','.join(cell_data) + '\n')
    f = open(SAVE_FILE_PATH + hw_name +'.csv', 'a')
    f.write(data)
    f.close()
    data = ''

# Get all submission pages
def iterateSubmissions(hw_name):
    
    # Wait for last page button to load
    time.sleep(1)

    # Get last page number
    pages = int(WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li.ivu-page-item')))[-1].text)

    # Clear data if a file with the same file name already exist
    open(SAVE_FILE_PATH + hw_name +'.csv', 'w').close()

    # Iterate through submission pages
    for i in range(1, pages + 1):        
        next_page = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.ivu-page-item[title = "' + str(i) + '"]')))
        next_page.click()
        # Wait for table data to refresh and display
        time.sleep(0.5)
        getSubmission(hw_name)
    driver.get(url)

# Main
def findAllHW():
    login()
    for hw_name in hw:
        loadSubmissionPage(hw_name)
        iterateSubmissions(hw_name)    

findAllHW()
