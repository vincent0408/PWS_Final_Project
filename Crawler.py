from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
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
hw = ['PWS Homework 6', 'PWS Homework 5']

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
def load_submission_page(hw_name):
    hw_keyword = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder = "Keyword')))
    hw_keyword.send_keys(hw_name)

    # Though using element_to_be_clickable, Selenium recieves clckable from GOM when it really isn't
    while(True):
        try:
            search_hw = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'i.ivu-icon-ios-search-strong')))
            search_hw.click()
            break
        except:
            continue

    press_hw = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, hw_name)))
    press_hw.click()
    time.sleep(1)
    # Necessary for PWS HWX
    find_hw_pw = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'input.ivu-input')))
    find_hw_pw.send_keys('pws')    
    find_hw_pw.send_keys(Keys.ENTER)    
    submissions_tab = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.ivu-icon-navicon-round')))
    submissions_tab.click()

original_text = None
# Get submission table data, 12*8
def get_submission(hw_name):
    global original_text
    while(True):
        try:
            # Get table and rows
            tr_collection = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'.ivu-table-row')))
            test_text = tr_collection[-1].find_elements_by_css_selector('td')[1].text
            if(test_text != original_text):
                original_text = test_text
                break
        except:
            continue
            
    data = ''
    
    # Write data to csv, 1 table at a time
    # Traditional way over pandas read_html due to the tbody tag in original HTML structure causing slower loading time if using pandas
    for row in tr_collection:

        # Improve concatenate speed using join instead of +=
        cell_data = [cell.text for cell in row.find_elements_by_css_selector('td')]
        data += (','.join(cell_data)+ ',' + hw_name  + '\n' )

    f = open(SAVE_FILE_PATH + hw_name +'.csv', 'a')
    f.write(data)
    f.close()
    data = ''

# Get all submission pages
def iterate_submissions(hw_name):

    open(SAVE_FILE_PATH + hw_name + '.csv', 'w').close()

    
    # Wait for last page button to load
    time.sleep(1)

    # Get last page number
    pages = int(WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'li.ivu-page-item')))[-1].text)

    # Iterate through submission pages
    for i in range(1, pages + 1):        
        next_page = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.ivu-page-item[title = "' + str(i) + '"]')))
        next_page.click()
        # Wait for table data to refresh and display
        #get_submission(hw_name)
    driver.get(url)

# Main
def find_all_hw():
    login()
    # Clear data if a file with the same file name already exist
    for hw_name in hw:
        load_submission_page(hw_name)
        iterate_submissions(hw_name)    

find_all_hw()
