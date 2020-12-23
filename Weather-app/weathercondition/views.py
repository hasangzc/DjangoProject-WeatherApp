from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
import requests
from bs4 import BeautifulSoup


def get_html_content(city):
    USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
    LANGUAGE = "en-US"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    city = city.replace(" ", "+")
    html_content = session.get(f'https://www.google.com/search?q=weather+{city}').text
    return html_content


def home(request):
    weather_data = None
    if "city" in request.GET:
        city = request.GET.get("city")
        html_content = get_html_content(city)
        soup = BeautifulSoup(html_content, "html.parser")
        weather_data = dict()
        weather_data["region"] = soup.find("div", attrs={"id": "wob_loc"}).text
        weather_data["daytime"] = soup.find("div", attrs={"id": "wob_dts"}).text
        weather_data["status"] = soup.find("span", attrs={"id": "wob_dc"}).text
        weather_data["temp"] = soup.find("span", attrs={"id": "wob_tm"}).text

    return render(request, "weathercondition/home.html", {"weather": weather_data})


