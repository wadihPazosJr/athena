import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# Start timer
start_time = time.time()

##### Web scrapper for infinite scrolling page #####
driver = webdriver.Chrome()
driver.get("https://www.nytimes.com/section/business")
time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = (
    1  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
)
screen_height = driver.execute_script(
    "return window.screen.height;"
)  # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script(
        "window.scrollTo(0, {screen_height}*{i});".format(
            screen_height=screen_height, i=i
        )
    )
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break

# Parse HTML
soup = BeautifulSoup(driver.page_source, "html.parser")

articles = soup.find_all("li", class_="css-112uytv")
import pandas as pd

# Sample data (empty lists for each attribute)
titles = []
authors = []
blurbs = []
urls = []

# Loop through each article
for article in articles:
    # Extract the values from the HTML tags
    title = article.find("h3", class_="css-1kv6qi e15t083i0").text.strip()
    author = article.find("span", class_="css-1n7hynb").text.strip()
    blurb = article.find("p", class_="css-1pga48a e15t083i1").text.strip()
    url = "https://www.nytimes.com" + article.find("a")["href"]

    # Append the values to the respective lists
    titles.append(title)
    authors.append(author)
    blurbs.append(blurb)
    urls.append(url)

# Create DataFrame
data = {"Title": titles, "Author": authors, "Blurb": blurbs, "URL": urls}
df = pd.DataFrame(data)

# Save DataFrame to CSV
csv_file_path = "business_data.csv"
df.to_csv(csv_file_path, index=False)

# Save DataFrame to JSON
json_file_path = "business_data.json"
df.to_json(json_file_path, orient="records")

# End timer and print run time
end_time = time.time()
print("Time taken in seconds: ", end_time - start_time)
