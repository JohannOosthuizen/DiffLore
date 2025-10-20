
import requests
from bs4 import BeautifulSoup

def main():
    """
    Main function to perform web research.
    """
    url = "https://www.google.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup.title.string)

if __name__ == "__main__":
    main()
