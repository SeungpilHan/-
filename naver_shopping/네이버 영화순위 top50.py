import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

movies = soup.select("#old_content > table > tbody > tr")

for movie in movies:
    movie_name = movie.select_one("td.title > div > a")
    movie_point = movie.select_one("td.point")
    if movie_name is not None:
        ranking = movie.select_one("td:nth-child(1) > img")["alt"]
        print(ranking, movie_name.text, movie_point.text)
