from django.http import HttpResponse,HttpResponseRedirect
from bs4 import BeautifulSoup
import requests
from django.urls import reverse
from django.shortcuts import render
import time
import pdb

def scrape(request):

    ctx = None
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        print(search_query)
        #pdb.set_trace()  
        r = requests.get(f"https://www.klekt.com/us/brands?search={search_query}")
        soup = BeautifulSoup(r.content, 'html.parser')

        prices = []
        spans = soup.find_all("span", attrs = {"itemprop" : "price"})
        if not spans:
            return HttpResponseRedirect(reverse("home"))
        for span in spans:
            price = span.text.strip()
            # Remove any dollar sign that might be prepended to the price
            price = price.replace('$', '')
            prices.append(price)
        
        items = soup.find_all("h3", {"class": "u-bold u-margin-bottom-none pod-name u-bodyLead"})
        items_title_list = []
        for item in items:
            items_title_list.append(item.text)

        items_urls = soup.find_all("a", attrs = {"class" : "pod-link"})
        product_urls_list = []
        for url in items_urls:
            urls = "https://www.klekt.com" + url['href']
            product_urls_list.append(urls)

        items_images = soup.find_all("img", attrs = {"class" : "pod-image o-image"})
        image_list = []
        for image in items_images:
            image_list.append(image['src'])

        items_list = []
        for i in range(len(items_title_list)):
            item_dict = {}
            item_dict['product_title'] = items_title_list[i]
            item_dict['price'] = prices[i]
            item_dict['product_detail_url'] = product_urls_list[i]
            item_dict['product_image'] = image_list[i]
            items_list.append(item_dict)

        # ctx = {"items_list": items_list}


        #             FROM WEBSITE https://stockx.com/
            # Set headers to mimic a more natural browsing behavior
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.google.com/',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'TE': 'Trailers',
        }

        # Set up a session to maintain cookies across requests
        session = requests.Session()

        # Access the search URL and wait for some time before proceeding
        search_url = f"https://stockx.com/search?s={search_query}"
        search_response = session.get(search_url, headers=headers)
        time.sleep(5)

        # Access the search results page and wait for some time before proceeding
        search_soup = BeautifulSoup(search_response.content, "html.parser")
        time.sleep(7)

        # Find all products on the search results page
        products = search_soup.find_all("div", class_="css-111hzm2-GridProductTileContainer")
        # Loop through each product and extract relevant information
        for product in products:
            name = product.find("p", class_="chakra-text css-3lpefb").text.strip()
            product_url = "https://stockx.com" + product.find("a", attrs = {"data-testid" : "RouterSwitcherLink"})['href']
            image_url = product.find("img")["src"]

            # Check if the price class is present
            if product.find("div", class_="tile-price"):
                price = product.find("div", class_="tile-price").text.strip()
            else:
                price = "--------"

            # Print out the information for each product
            # print("Name:", name)

            item_dict2 = {}

            item_dict2['product_title'] = name
            item_dict2['price'] = price
            item_dict2['product_detail_url'] = product_url
            item_dict2['product_image'] = image_url
            items_list.append(item_dict2)
            ctx = {"items_list": items_list}

        #     print()

    return render(request, 'scraper_app/index.html', ctx)


