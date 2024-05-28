import requests
from bs4 import BeautifulSoup as bf


cookies = {
    'MoodleSession': 'b1btr2q4510pgtpu20rnb95hol',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://moodlelms.eelu.edu.eg/course/view.php?id=1641',
    'DNT': '1',
    'Connection': 'keep-alive',
    # 'Cookie': 'MoodleSession=b1btr2q4510pgtpu20rnb95hol',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
}

params = {
    'id': '32316',
}

response = requests.get('https://moodlelms.eelu.edu.eg/mod/quiz/view.php', params=params, cookies=cookies, headers=headers)
soup=bf(response.content,"html.parser")
z = soup.find_all("p")
print(z)

outfile = open("modr.html", "a")
print("doing page 1 ")
outfile.write("\n".join(str(i) for i in z))
print("page 1 done")
outfile.close()

for j in range(2,3):
    z=[]
    n = response+str(j)+"/"
    html = requests.get(n).content
    so = bf(html,"lxml")
    z = so.find_all("p")
    outfile = open("modr.html", "a")
    print("doing page ",j)
    outfile.write("\n".join(str(i) for i in z))
    print("page ",j," complete")
    outfile.close()
