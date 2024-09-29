from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

# Set the path to the chromedriver
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")  # Ensure this is set in your .env file

def scrape_website(website):
    print("Starting local Chrome WebDriver...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    service = Service(executable_path=CHROMEDRIVER_PATH)
    
    # Start the WebDriver locally
    with webdriver.Chrome(service=service, options=chrome_options) as driver:
        driver.get(website)
        print("Waiting for captcha to solve...")  # If there's captcha, handle it here
        html = driver.page_source
        return html


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
