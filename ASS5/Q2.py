from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

chrome_options=Options()
chrome_options.add_argument("--headless")
driver=webdriver.Chrome(options=chrome_options)

driver.get("https://www.sunbeaminfo.in/internship")
print("Page Title\n",driver.title)
driver.implicitly_wait(5)

print("Internship Information\n")
para = driver.find_elements(By.CSS_SELECTOR, ".main_info.wow.fadeInUp")
for p in para:
    print(p.text)

print("_Internship Batches-")
table_body=driver.find_element(By.TAG_NAME,"tbody")
table_rows=driver.find_elements(By.TAG_NAME,"tr")

batches=[]

for row in table_rows:
    cols=row.find_elements(By.TAG_NAME,"td")
    
    if len(cols) < 8:
        continue

    
    info={
        "sr":cols[0].text,
        "batch":cols[1].text,
        "batch duration":cols[2].text,
        "start date":cols[3].text,
        "end date":cols[4].text,
        "time":cols[5].text,
        "fees":cols[6].text,
        "download":cols[7].text
    }

    batches.append(info)


print(json.dumps(batches, indent=4))

driver.quit()