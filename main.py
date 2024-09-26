from youtube_scraper import fetch_youtube_data
from instagram_scraper import scrape_instagram_data
from credentials_manager import prompt_credentials, login
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from data_saver import save_data_to_excel

def main():
    # YouTube data
    yt_api_key = input("Enter your YouTube Data API Key: ")
    yt_channel = input("Enter YouTube channel name: ")
    num_videos = int(input("Enter the number of YouTube shorts to fetch: "))

    yt_captions, yt_views = fetch_youtube_data(yt_api_key, yt_channel, num_videos)
    
    # Instagram data
    insta_username = input("Enter the Instagram username to scrape: ")
    num_reels = int(input('How many reels do you want to scrape (10-50 recommended): '))

    # Selenium setup for Instagram
    username, password = prompt_credentials()
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=3")
    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    bot = webdriver.Chrome(service=service, options=options)
    bot.set_page_load_timeout(15)

    login(bot, username, password)
    
    insta_captions, insta_views = scrape_instagram_data(bot, insta_username, num_reels)
    bot.quit()

    # Save the combined data to Excel
    save_data_to_excel(yt_captions, yt_views, insta_views)

if __name__ == '__main__':
    main()
