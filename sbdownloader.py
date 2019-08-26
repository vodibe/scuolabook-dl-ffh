from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.firefox.options import Options

import os
import sys
import re
from time import sleep
import getpass        
import urllib.request
import img2pdf

##########################################################################
# CUSTOM SETTINGS: edit this BEFORE running the program.

# 1. Specify your operating system user name
osuser = "user" # <-- edit this

# 2. Specify Geckodriver path
#    REMEMBER TO ADD ANOTHER BACKSLASH (\)
#    for example driver_path = "C:\\Users\\user\\Desktop\\geckodriver.exe"
driver_path = "C:\\Python37\\geckodriver-v0.24.0-win64\\geckodriver.exe"

# 3. (OPTIONAL) Edit the output path.
#    REMEMBER TO ADD ANOTHER BACKSLASH (\)
bookpath = "C:\\\\Users\\"+osuser+"\\Desktop\\"
##########################################################################

def progressBar(value, endvalue, bar_length=20):
        percent = float(value) / endvalue
        arrow = '#' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))
        print(str(value)+"/"+str(endvalue)+" ["+arrow+spaces+"] %.1f%% \r" % (percent * 100), end="\r")

#setting up firefox headless
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path=driver_path)

print("\nScuolabook Downloader FFH")
print("Author: brearlycoffee.cf")

driver.get("http://webapp.scuolabook.it/")

#request credentials
print("\nInsert your Scuolabook account credentials:")
eml = input('Email:')
pwd = getpass.getpass("Password:")

#loading values
usr_box = driver.find_element_by_id('email')
usr_box.send_keys(eml)

pwd_box = driver.find_element_by_id('pass')
pwd_box.send_keys(pwd)

#click login button
login_button = driver.find_element_by_name("send")
login_button.click()
sleep(2)

#------------------------------------------------

bookcount = 0
codes = []
pages = []

all_books = driver.find_elements_by_xpath("//div[@class='book']")
bookcount = len(all_books)
print("\n[Your Library - "+str(bookcount)+" books found]\n")
all_details = driver.find_elements_by_xpath("//div[@class='book']/div[@class='row-fluid']/div[@class='span9']")

if bookcount == 0:
    try:
        try: #return any errors or messages, then exit
            message_box = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".error-msg")))
        except:
            message_box = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#advice-validate-email-email")))
        
        print("The website returned the following error:\n"+message_box.text)
        print("\nClosing...")
        driver.close()
        sys.exit(0)
    except:
        print("No books have been found!") 
        print("\nClosing...")
        driver.close()
        sys.exit(0)
else:    
    for i in range(len(all_books)):
        code = all_books[i].get_attribute("id")[5:]
        codes.append(code)
        
				#print details of books
        title = all_details[i].find_element_by_tag_name("h2")
        author = all_details[i].find_element_by_class_name("authors")
        page = all_details[i].find_element_by_class_name("details")
        
        print("["+code+"] ", title.text)
        
        #print authors and pages number
        print("        "+author.text)
            
        npages = re.search("\d+", page.text)
        npages = npages.group(0)
        print("        Pages number: "+npages)
        pages.append(npages)

#------------------------------------------------

dledpages = 0
lastdled = ""
countsl = 0
arraychoice = -1

notvalid = True

while notvalid:	# request a code until a valid one is typed
    codein = input('\nInsert the book ID:')
    codein = codein.strip()
    for i in range(len(codes)):
        if codein == codes[i]:
            arraychoice = i
            notvalid = False
            break
    if notvalid:
        print("Insert a valid book ID!")
    
driver.find_element_by_id("book_"+codein).click()
driver.switch_to.window(driver.window_handles[1])

bookpath = bookpath+codein+"\\"
try:  
    os.mkdir(bookpath)
except OSError:  
    print("Unable to create directory or directory already created!\n"+bookpath+"\n")
else:  
    print ("Successfully created the directory: "+bookpath+"\n")
    
page_box = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME, "page-num")))
page_box.clear()
page_box.send_keys("cov")
page_box.send_keys(Keys.RETURN)
sleep(2)

while dledpages < int(pages[arraychoice])+2:
    if dledpages == 0:
        lastdled = "-1"

				#wait for div element
    try:
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".p"+str(dledpages+1))))
    except:
        dledpages = dledpages + 1
    else: 
        try:
            imgselector = ".p"+str(dledpages+1)+" > img:nth-child(2)"
            img = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, imgselector)))
        except:
            imgselector = ".p"+str(dledpages+1)+" > img:nth-child(3)"
            img = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, imgselector)))
      
        imglink = ""
        imglink = img.get_attribute("src")
        
				#get file name from image link
        countsl = 0
        dled = ""
        for i in range(len(imglink)):
            if(imglink[i] == "/"):
                countsl = countsl+1
                
                if countsl == 6:
                    i = i+1
                    while imglink[i] != ".":
                        dled = dled + imglink[i]
                        i = i+1
                    break
        
        filename = ""
        filename = (len(pages[arraychoice])-len(str(dledpages+1)))*"0"+str(dledpages+1)
        
				#avoid repeated pages
        if int(dled) != int(lastdled):        
            urllib.request.urlretrieve(imglink, bookpath+filename+".jpg")
            lastdled = dled
            #print("Download: "+str(dledpages+1)+"/"+pages[arraychoice]+" - %.1f %%" % ((dledpages+1)*100/int(pages[arraychoice])))  
            
            dledpages=dledpages+1
            
            if(dledpages <= int(pages[arraychoice])):
                progressBar(dledpages,int(pages[arraychoice]),20)
            
            driver.find_element_by_css_selector('body').send_keys(Keys.RIGHT)

print("Book #"+str(codein)+" has been correctly downloaded.")
driver.close()

#--------------------------------------------------------

print("Merging everything into single PDF")

imagelist = os.listdir(bookpath)
for i in range(len(imagelist)):
    imagelist[i] = bookpath+imagelist[i]
    
print("This action requires several minutes, please wait...\n")
with open(bookpath+str(codein)+".pdf","wb") as f:
    f.write(img2pdf.convert(imagelist))

print("Deleting images...\n")
for i in range(len(imagelist)):
    os.remove(imagelist[i])

print("Finished! Check: "+bookpath+str(codein)+".pdf")
