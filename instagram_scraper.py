import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

TIMEOUT = 15

def parse_view_count(view_text):
    view_text = view_text.replace(',', '')
    if 'K' in view_text:
        return int(float(view_text.replace('K', '')) * 1000)
    elif 'M' in view_text:
        return int(float(view_text.replace('M', '')) * 1000000)
    else:
        return int(view_text)

def scrape_reel_views(bot, username, num_reels=10):
    bot.get(f"https://www.instagram.com/{username}/reels/")
    time.sleep(3.5)

    WebDriverWait(bot, TIMEOUT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div._aajy"))
    )

    reel_views = []
    last_height = bot.execute_script("return document.body.scrollHeight")

    while len(reel_views) < num_reels:
        bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        reel_boxes = bot.find_elements(By.CSS_SELECTOR, "div._aajy")

        for box in reel_boxes:
            if len(reel_views) >= num_reels:
                break

            try:
                view_element = box.find_element(By.CSS_SELECTOR, "span.xdj266r")
                view_text = view_element.text.strip()
                views = parse_view_count(view_text)
                reel_views.append(views)
            except:
                continue

        new_height = bot.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return reel_views

def scrape_instagram_data(bot, username, num_reels):
    views = scrape_reel_views(bot, username, num_reels)
    return [], views  # No captions in this case
