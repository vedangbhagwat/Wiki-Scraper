import requests
from bs4 import BeautifulSoup
import re
import datetime

URL = "https://en.wikipedia.org/wiki/Brad_Pitt"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <title>{0}</title>
</head>
<body>
    <h1>{0}</h1>
    <p>Hi <br>
    
    My name is {1}. <br>
    
    I was born on {2} in {3}, and I am {4} years old. <br>
    
    I look like this: <br>
    <img src="https://{5}"> <br>
    <br>
    I attended {6} and I have worked as {7} from {8}. <br>

    I was married to {9} and I have {10} children. <br>

    My relative's name is {11}. <br>

    </p>
    
</body>
</html>
'''

response = requests.get(URL)

if response.status_code == 200:
    content = response.content
    soup = BeautifulSoup(content , 'html.parser')
    tag = soup.find('table' , {'class':'infobox biography vcard'})
    name = tag.find('th', {'class':"infobox-above"}).text
    
    birthname = tag.find('div', {'class':"nickname"}).text
    date = tag.find('span', {'class':"bday"}).text
    dob = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%B %d, %Y')

    age = tag.find('span', {'class':"noprint ForceAgeToShow"}).text
    age_match = re.search(r'\d+', age)
    age = int(age_match.group())

    place = tag.find('div', {'class':"birthplace"}).text
    
    image = str(tag.find('a', {'class':"image"}))
    url_match = re.search(r'srcset="(.*?)"', image)
    url = url_match.group(1).split()[0]

    uni = tag.find("a", text="University of Missouri").text

    occu = tag.find("th", text="Occupations")
    occu = occu.find_next_sibling("td").text

    spouses = tag.find('th', text='Spouses').parent
    spousess = []
    for spouse in spouses.find_all('a'):
        spousess.append(spouse.text)
    spousess.pop()

    years = tag.find("th", text="Years active").parent
    ya = years.find("td").text.strip()

    child = tag.find("th", text="Children").parent
    num_children = child.find('td').text.strip()

    relatives = tag.find("th", text="Relatives").parent
    rel = relatives.find('td').text.strip()

    with open("index.html", "w") as f:
        f.write(HTML_TEMPLATE.format(name, birthname, dob, place, age, url, uni, occu, ya, spousess, num_children, rel))

else:
    print("That didn't work!")

