#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time, pickle, os
from datetime import date

curDir = os.getcwd()
mimeTypeFile = curDir + "/mimeTypes"

# ~dlDir~ specific firefox auto download file path
# ensure ~dlDir~ is empty, download file will be first saved in ~dlDir~ then
# moved to ~HWDir/$studentName~
dlDir = curDir + "/Downloads"
os.system("[[ -d " + dlDir + " ]] || mkdir -p " + dlDir)
HWDir = curDir + "/HW/"
os.system("[[ -d " + HWDir + " ]] || mkdir -p " + HWDir)

def yes_or_no(question):
    while "the answer is invalid":
        reply = input(question+' (y/n): ').lower()
        if reply == 'y':
            return True
        if reply == 'n':
            return False
        else:
            print('Invalid Input')

# load all mimeType, some pdf would still not recoginzed, user should manually
# click the ~save for all~ checkin box.
mimeType = []
with open(mimeTypeFile) as mt:
    for line in mt:
        mimeType.append(line.strip())

fp = webdriver.FirefoxProfile()

fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir", dlDir)
fp.set_preference("browser.helperApps.alwaysAsk.force", False)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", ','.join(mimeType))

browser = webdriver.Firefox(firefox_profile=fp)
if not yes_or_no('Direct to download webpage in the opened firefox windows, done?'):
    exit()

wait = WebDriverWait(browser, 2)
flag = True
while flag:
    cnt = len(browser.find_elements_by_class_name('gradeAttempt'))
    print(cnt, " entries found in this webpage\n")
    emptyCnt = 0
    for i in range(cnt):
        entry = browser.find_elements_by_class_name('gradeAttempt')[i]
        name = entry.text.split(" ")[0]
        entry.click()
        try:
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "dwnldBtn")))
        except:
            print("!! Cannot find a file to download")
            emptyCnt += 1
            continue
        files = browser.find_elements_by_class_name("dwnldBtn")
        for f in files:
            f.click()
        while len(os.listdir(dlDir)) < len(files) or any([fn.endswith(".part") for fn in os.listdir(dlDir)]):
            time.sleep(0.5)
        newdir = HWDir + name
        os.system("[[ -d " + newdir + " ]] || mkdir -p " + newdir)
        os.system("mv " + dlDir + "/* " + newdir)
        browser.back()
        print(i, name, sep='\t')
    print("\n", cnt-emptyCnt, " success, ", emptyCnt, " fail")
    flag = yes_or_no("redownloaded?")
browser.quit()
