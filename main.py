 ##!pip install selenium
!pip install selenium==4.2.0 --force-reinstall
!apt-get update 
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin

from datetime import date

import re
from google.colab import auth
import gspread
from google.auth import default
from oauth2client.client import GoogleCredentials
import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.expected_conditions import staleness_of

strSheetURL='1gRHY2uH1fXkCQ24x_unQQgfsoKuU6C1s90iidvnFQXs'
wanChaiBuy2MTo4MUrl='https://www.house730.com/buy/hma160t1p1/'
wanChaiBuy4MTo6MUrl='https://www.house730.com/buy/hma160t1p2/'
kowloonBayBuy2MTo4MUrl='https://www.house730.com/buy/hkp050t1p1/'
kowloonBayBuy4MTo6MUrl='https://www.house730.com/buy/hma005t1p2/'

wanChaiRent5KTo10KUrl='https://www.house730.com/rent/hma160t1p3/'
wanChaiRent10KTo20KUrl='https://www.house730.com/rent/hma160t1p4/'
kowloonBayRent5KTo10KUrl='https://www.house730.com/buy/hma005t1p1/'
kowloonBayRent10KTo20KUrl='https://www.house730.com/rent/hma005t1p4/'


##############################################################
def wait_for_page_load(browser, timeout=30):
    old_page = browser.find_element_by_tag_name('html')
    yield
    WebDriverWait(browser, timeout).until(
        staleness_of(old_page)
    )
##############################################################
def filter_non_digits(string: str) -> str:
    result = ''
    for char in string:
        if char in '1234567890':
            result += char
    return result 
##############################################################    

####################### house 28 ################################
def findCountForHouse28(strUrl: str, data_id: str) ->str:
  driver.get(strUrl)#put here the adress of your page
  linkElems = driver.find_elements_by_xpath("//a[@href]")
  for linkElem in linkElems:
    if linkElem.get_attribute("data-id")==data_id:
      print(linkElem.get_attribute("data-id"))
      clickLinks=linkElem
      #for clickLink in clickLinks:
        #clickLink.click()
        #break
      linkElem.click()
      break

  wait_for_page_load(driver,20) 
  elem = driver.find_element_by_id("search_results_loader")#put here the content you have put in Notepad, ie the XPath
  tempResult = filter_non_digits(elem.text[0:10])
  return tempResult
##############################################################  


####################### House 730 ################################
def findCountForHouse730(strUrl: str) ->str:
  driver.get(strUrl)#put here the adress of your page
  elem = driver.find_element_by_class_name("fred")#put here the content you have put in Notepad, ie the XPath
  #tempResult = filter_non_digits(elem.text[0:10])
  return elem.text
##############################################################  


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

resultWanChaiBuy2Mto4M=findCountForHouse730(wanChaiBuy2MTo4MUrl)
print("Wan Chai 2M-4M Buy="+resultWanChaiBuy2Mto4M)

resultWanChaiBuy4Mto6M=findCountForHouse730(wanChaiBuy4MTo6MUrl)
print("Wan Chai 4M-6M Buy="+resultWanChaiBuy4Mto6M)

resultKowloonBayBuy2Mto4M=findCountForHouse730(kowloonBayBuy2MTo4MUrl)
print("Kowloon Bay 2M-4M Buy="+resultKowloonBayBuy2Mto4M)

resultKowloonBayBuy4Mto6M=findCountForHouse730(kowloonBayBuy4MTo6MUrl)
print("Kowloon Bay 4M-6M Buy="+resultKowloonBayBuy4Mto6M)

resultWanChaiRent5Kto10K=findCountForHouse730(wanChaiRent5KTo10KUrl)
print("Wan Chai 5K-10K Rent="+resultWanChaiRent5Kto10K)

resultWanChaiRent10Kto20K=findCountForHouse730(wanChaiRent10KTo20KUrl)
print("Wan Chai 10K-20K Rent="+resultWanChaiRent10Kto20K)

resultKowloonBayRent5Kto10K=findCountForHouse730(kowloonBayRent5KTo10KUrl)
print("Kowloon Bay 5K-10K Rent="+resultKowloonBayRent5Kto10K)

resultKowloonBayRent10Kto20K=findCountForHouse730(kowloonBayRent10KTo20KUrl)
print("Kowloon Bay 10K-20K Rent="+resultKowloonBayRent10Kto20K)

#1. Authorize
#auth.authenticate_service_account
auth.authenticate_user()

!cat adc.json


# 2. credentials for google sheets
creds, _ = default()

# 3. authotizing the connection
#gc = gspread.authorize(creds)
gc = gspread.authorize(creds)

#4. Connecting 
worksheet = gc.open_by_key(strSheetURL).sheet1

#5. Exporting data to get_all_values gives a list of rows.
rows = worksheet.get_all_values()

# 6. Using pandas to convert to a DataFrame and render.
df = pd.DataFrame.from_records(rows)

rowCount=len(df.index)
print("rowCount"+str(rowCount))
# 
# yyyy-mm-dd
today=date.today()
strToday = today.strftime("%Y-%m-%d")
print("df[0][rowCount-1]="+str(df[0][rowCount-1]))


if str(df[0][rowCount-1])!=strToday:
  currentRow=rowCount+1
else:
  currentRow=rowCount

worksheet.update_cell(currentRow, 1,strToday)
worksheet.update_cell(currentRow, 2,resultWanChaiBuy2Mto4M )
worksheet.update_cell(currentRow, 3,resultWanChaiBuy4Mto6M )
worksheet.update_cell(currentRow, 4,resultKowloonBayBuy2Mto4M )
worksheet.update_cell(currentRow, 5,resultKowloonBayBuy4Mto6M )
worksheet.update_cell(currentRow, 6,resultWanChaiRent5Kto10K)
worksheet.update_cell(currentRow, 7,resultWanChaiRent10Kto20K)
worksheet.update_cell(currentRow, 8,resultKowloonBayRent5Kto10K )
worksheet.update_cell(currentRow, 9,resultKowloonBayRent10Kto20K)

driver.close()
