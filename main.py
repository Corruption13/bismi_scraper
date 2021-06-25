from bs4 import BeautifulSoup
import chromedriver_autoinstaller
import time
from selenium import webdriver

chromedriver_autoinstaller.install()    # Auto Install WD

# DEFINE
PRODUCT_NAME_HTML_CLASS = "titleMain mb-2 c-pointer text-overflow"
PRODUCT_PRICE_HTML_CLASS = "wPrice2"
DISABLE_IMAGE_LOADING = True    # Less Network Use.
SLEEP=3 # Anti DDOS Protection
TIMEOUT=15

#File Initialisation
file_in = open("input.csv", "r")    # Category, URL$page=, total_pages
file_out = open("output.csv", "w+") # Product Name, Price, Category
file_out.write("Product Name, Price, Category\n") # Initialising CSV with Table Headers

def main():

    print("Ignore any warnings below.\n\n")  
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    if DISABLE_IMAGE_LOADING:
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get('https://www.bismideal.com/Grocery/')
    
    inp = input("\n\n!!!\n\nInput the pin code in the popup browser and press Enter key to start scraping: ")
    # To initialise pincode with current browser session.
    print("Starting..\n")

    for line in file_in:
        time.sleep(SLEEP)   
        items = line.split(",") 
        category = items[0]
        url = items[1]
        page_count = items[2]
        print("\n\nCategory:", category+"\n")

        for page in range(int(page_count)):    
            print(str(page+1)+"/"+page_count)
            page_scraper(driver, 1, category, url+str(page+1))   # Single Page Scraper function.

    print("Scraping Completed.")        
    file_out.close()
    driver.quit()


def page_scraper(driver, sleep, category, url):

    driver.get(url)
    time.sleep(sleep) # Anti DDOS Protection.
    html = driver.page_source
    soup = None
    soup = BeautifulSoup(html, features="lxml")
    
    # Table here
    product_name = soup.find_all("div", class_=PRODUCT_NAME_HTML_CLASS)    # Defined at top of program.
    product_price = soup.find_all("span", class_=PRODUCT_PRICE_HTML_CLASS) 
    # product_weight = etc
    #
    blah = product_name # idk what this line does it breaks if I remove this line haha.
    if not product_name:
        print("No Product Found, Reloading " + sleep + " [max: " + TIMEOUT + "]") 
        if sleep<TIMEOUT:
            page_scraper(driver, sleep+1, category, url)
        else:
            print("Timed out, Skipping page.")
    else:
        for f, b in zip(product_name, product_price):
            print(f.text + " " + b.text) 
            file_out.write(f.text + ", " 
                + b.text + ", " 
                + category + "\n")



if __name__ == "__main__":
    main()