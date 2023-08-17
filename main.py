import requests
from bs4 import BeautifulSoup
import lxml
import smtplib

MY_EMAIL = "jintao.helsinki@gmail.com"
PASSWORD = "Your app password"
URL = "https://www.amazon.de/-/en/ARZOPA-Portable-Monitor-External-Black-1/dp/B092KKLH93?ref_=Oct_d_obs_d_429868031_0&pd_rd_w=s4Trn&content-id=amzn1.sym.e29f2335-2e49-4147-8cf3-d7e9bd9a576a&pf_rd_p=e29f2335-2e49-4147-8cf3-d7e9bd9a576a&pf_rd_r=TKAF4A3YWFAQBW99WN77&pd_rd_wg=dvMUi&pd_rd_r=8cd8212c-eaa3-448e-b4f8-e51cee1fb7ad&pd_rd_i=B092KKLH93"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,fi;q=0.7",
}

response = requests.get(url=URL, headers=header)
response.raise_for_status()
html_text = response.content

soup = BeautifulSoup(html_text, "lxml")
# print(soup.prettify())
title = soup.find(id="productTitle").getText().strip()


price_round = soup.find(class_="a-price-whole").getText()
price_fraction = soup.find(class_="a-price-fraction").getText()
price = float(price_round + price_fraction)

if price <= 150:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="jintao.aalto@gmail.com",
            msg=f"Subject: Amazon Price Alert! \n\n{title} is now {price} euros!\nlink: {URL}"
        )
        connection.close()