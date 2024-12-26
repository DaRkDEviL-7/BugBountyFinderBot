import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.text
    except requests.RequestException as e:
        return f"Error scraping the website: {e}"

def scrape_hackerone():
    url = "https://hackerone.com/bugs"  # Replace with the actual URL you want to scrape
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        soup = BeautifulSoup(response.content, "html.parser")
        # Add your parsing logic here
        # For example, to extract all bug titles:
        bug_titles = [h2.text for h2 in soup.find_all("h2", class_="bug-title")]
        return bug_titles
    except requests.RequestException as e:
        return f"Error scraping HackerOne: {e}"

def scrape_bugcrowd():
    url = "https://bugcrowd.com/programs"  # Replace with the actual URL you want to scrape
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        soup = BeautifulSoup(response.content, "html.parser")
        # Add your parsing logic here
        # For example, to extract all program names:
        program_names = [h3.text for h3 in soup.find_all("h3", class_="program-name")]
        return program_names
    except requests.RequestException as e:
        return f"Error scraping Bugcrowd: {e}"
