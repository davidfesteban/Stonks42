import requests
from bs4 import BeautifulSoup


class ScrapService:
    def run(self):
        url = "https://example.com"

        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Step 2: Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Step 3: Use BeautifulSoup to find elements (like you would with Jsoup)
            # Example: Finding all paragraph tags
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                print(p.text)

            # Example: Selecting elements with a specific class
            headings = soup.find_all("h2", class_="headline")
            for heading in headings:
                print(heading.text)
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
