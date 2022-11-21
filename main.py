"""This is a program designed to scrape the web through brute force

I wanted to get my feet wet in machine learning and web scraping for data to feed to AI,
so I built this program in hopes of creating a branching system of search and collect.

The user inputs a url and then can navigate through the browser, and all urls on pages clicked as well
as all html from those pages are saved into separate files. Pretty open ended for now,
but the goal is to create something that essentially starts somewhere and searches a whole website for its data.

Eventually I want to make it so the program can search the whole internet for data, or attempt to, by branching from
site to site, saving lists of urls to visit and continue branching from there. I will add visited urls to a visited url
file and continue moving forward, making sure not to revisit past sites.

Why scrape? Just to learn, and for fun!

Potential uses: Tell a web developer when their page has urls on some pages but not on others, maybe a blog
link is on one page but missing everywhere else, it will show up on one of the separate records"""
import time
import urllib
from datetime import datetime

from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen

# INSTANCE VARIABLES

# this is the "home page" url for a particular run, something for the program to fall back to if needed
branch_start = ""

# starts the main loop
def main():
    url = input("Please enter a url to search")
    print(url[0:4])
    # fast and loose attempt to allow a user to type "google" and get to https://google.com
    if url[0:4] != "http":
        url = "https://" + url

    if ".com" not in url:
        url += ".com"
    # not the right way
    #branch_start = url

    # we're opening Chrome with Selenium
    driver = webdriver.Chrome()
    driver.get(url)
    link_text = "start"
    while link_text != "" or link_text != "quit":
        link_text = input("Type the name of the button you wish to press on this page")
       # if link_text == "home":
           # driver.get(branch_start)
           # continue

        # an html element, hopefully clickable
        element = None

        # nested try excepts to try to click on different elements, this is not great lol, but it works at a basic level
        try:
            element = driver.find_element("partial link text", link_text)
        except:
            try:
                element = driver.find_element("tag name", "input")
            except:
                try:
                    element = driver.find_element("tag name", "p class")
                except:

                    try:
                        element = driver.find_element("tag name", "<a class")
                    except:
                        print("Couldn't find that button, try another by entering the text on the button")
        # if we found a clickable element
        if element != None:
            element.click()
            # sometimes the web page denies my request to get in, so for now I just skip that URL, but this needs to be
            # fixed
            try:
                f = urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
                page = urllib.request.urlopen(f)
                time.sleep(.1)
                html = page.read().decode("utf-8")
                soup = BeautifulSoup(html, "html.parser")
                file = open("raw_data.txt", "w",encoding="utf-8")
                time.sleep(.1)
                file.write(str(soup))
                file.close()
                time.sleep(.1)
                save_urls(soup,driver)
                check_for_my_name(soup)

            except:
                pass
        else:
            print("No element found")

        time.sleep(.5)



#print(soup)


# eventually need to reform this method to allow for any phrase
def check_for_my_name(soup):
    first_name = "kory"
    last_name = "stennett"
    if first_name.casefold() in str(soup):
        if last_name.casefold() in str(soup):
            print("True")

# saving the urls to a file to be used later
def save_urls(soup,driver):
    file = open("stripped_urls.txt", "r+")
    now = datetime.now()
    urls = file.read().split()
    current_time = now.strftime("%H:%M:%S")
    file.write("\n\nNew record added at: " + current_time + "  |  On page "+ driver.title +"\n\n")

    for link in soup.find_all('a'):

        if link != None:
            try:
                # only send it to the file if it actually starts with http because we can almost always assume that will
                # be a link, not perfect though
                if str(link.get('href')[0:4]) == "http" and str(link.get('href')) not in urls:
                    print(link.get('href'))
                    file.write(str(link.get('href')) + "\n")
            except:
                pass
    file.close()
    time.sleep(.1)


main()