from fastapi import FastAPI, HTTPException
import requests
from bs4 import BeautifulSoup


app = FastAPI()\

@app.get("/")
def root():
    return {"message": "blah blah"}

@app.post("/wikipedia_personal_info")
async def wikipedia_personal_info(url: str):
    # Make sure the URL is a valid Wikipedia page
    if not url.startswith("https://en.wikipedia.org/wiki/"):
        raise HTTPException(status_code=400, detail="Not a valid Wikipedia URL")

    # Retrieve the page HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the personal information from the page
    personal_info = {}
    for table in soup.find_all("table", class_="infobox"):
        for row in table.find_all("tr"):
            if row.th and row.th.text in ["Born", "Born:", "Born on", "Born in"]:
                personal_info["born"] = row.td.text.strip()
            elif row.th and row.th.text == "Alma mater":
                personal_info["Alma mater"] = row.td.text.strip()
            elif row.th and row.th.text == "Occupations":
                personal_info["Occupations"] = row.td.text.strip()
            elif row.th and row.th.text == "Years active":
                personal_info["Years active"] = row.td.text.strip()
            elif row.th and row.th.text == "Spouses":
                personal_info["Spouses"] = row.td.text.strip()
            elif row.th and row.th.text == "Children":
                personal_info["Children"] = row.td.text.strip()
            elif row.th and row.th.text == "Relatives":
                personal_info["Relatives"] = row.td.text.strip()

    for key, value in personal_info.items():
        value = value.replace('\u200b', ' ').replace('\xa0', ' ').replace('\n', '')
        personal_info[key] = value

    # Return the personal information
    return personal_info