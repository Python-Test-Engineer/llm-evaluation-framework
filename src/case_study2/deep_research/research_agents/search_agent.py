from agents import Agent, function_tool
from bs4 import BeautifulSoup
import requests


@function_tool
def url_scrape(url: str) -> str:
    """
    Scrapes a website for it's contents given a url
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        try:
            soup = BeautifulSoup(response.text, "html.parser")

            for script in soup(["script", "style"]):
                script.extract()

            text = soup.get_text(separator=" ", strip=True)

            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = " ".join(chunk for chunk in chunks if chunk)

            return text[:5000] if len(text) > 5000 else text
        except ImportError:
            return response.text[:5000]
    except Exception as e:
        return f"Failed to scrape content from {url}: {str(e)}"


SEARCH_AGENT_PROMPT = """
    You are a research assistant. Given a URL and its title, you will analyze the content of the URL.
    ONLY use English language content and English Alphabet characters. 
    Produce a concise summary of the information. The summary must be 2 paragraphs.
    Capture the main points.
    Write succinctly, no need to have complete sentences or perfect grammar. This will be consumed by someone synthesizing a report, so it's vital you capture the essence and ignore any fluff. Do not include any additional commentary other than the summary itself."""


search_agent = Agent(
    name="Search Agent",
    instructions=SEARCH_AGENT_PROMPT,
    tools=[url_scrape],
    model="gpt-4o-mini",
)
