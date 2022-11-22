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
import random
import time
import urllib
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen

# INSTANCE VARIABLES

# this is the "home page" url for a particular run, something for the program to fall back to if needed
branch_start = ""

# starts the main loop
def main():
    file = open("stripped_urls.txt","w")
    file.close()
    file = open("visited_urls.txt","w")
    file.close()
    url = input("Please enter a url to search, if you don't enter \"https:\\\\\" or \".com\", this may not work.")
    phrase_to_look_for = input("Please enter a phrase, name, or any sort of word to look for on the internet.")
    # fast and loose attempt to allow a user to type "google" and get to https://google.com
    if url[0:4] != "http":
        url = "https://" + url

    #if ".com" not in url:
        #url += ".com"
    # not the right way
    #branch_start = url

    chrome_options = Options()
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox") # linux only
    chrome_options.add_argument("--headless")
    # we're opening Chrome with Selenium

    driver = webdriver.Chrome(options=chrome_options)
    check_google(driver, phrase_to_look_for)
    wait(.5)
    try:
        driver.get(url)
    except:
        print("PROBABLY DIDN'T INCLUDE .com AT END OF URL, USING REDDIT AS STARTING POINT")
        driver.get("https://reddit.com")

    times_phrase_found = 0
    """link_text = "start"
    while link_text != "" or link_text != "quit":
        #link_text = input("Type the name of the button you wish to press on this page")
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
            # fixed"""
    while True:
        try:
            f = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
            try:
                page = urllib.request.urlopen(f)
            except:
                url = "https://reddit.com"
                continue
            print("OPENING PAGE")
            wait(.01)
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            past_url = url
            save_urls(soup, driver, past_url)
            print("Saving URLS")
            time.sleep(.01)
            print("CHECKING FOR PHRASE")
            phrase_check = check_for_phrase(phrase_to_look_for, soup)
            times_phrase_found += phrase_check
            print("Times phrase found: " + str(times_phrase_found))
            if phrase_check > 0:
                file = open("raw_data.txt", "a", encoding="utf-8")
                # time.sleep(.1)
                file.write(str(soup))
                file.close()
                print("RAW DATA SAVED")
                wait(.01)

            time.sleep(.01)
            print("Current url: " + url)
            time.sleep(.01)
            url = fetch_next_url()
            time.sleep(.01)
            try:
                f = urllib.request.Request(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
                page = urllib.request.urlopen(f)
            except:
                # sometimes it just won't load the next url we've chosen, so i'm trying to find ways past that
                # time.sleep(.1)
                f = urllib.request.Request(past_url, headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
                page = urllib.request.urlopen(f)
            time.sleep(.01)

        except:
            # twitter is not letting me access their site so if we hit something
            # like that, this block should handle that
            # unelegant solution = go to a message board = better chance to find phrase
            url = fetch_next_url()
            print("Can't reach this page, opening a forum")
            f = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
            page = urllib.request.urlopen(f)

        #time.sleep(.5)



#print(soup)

def check_page(url,driver,phrase_to_look_for):
    try:
        f = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        try:
            page = urllib.request.urlopen(f)
        except:
            url = "https://reddit.com"
            f = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
            page = urllib.request.urlopen(f)
        print("OPENING PAGE")
        wait(.01)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        past_url = url
        save_urls(soup, driver, past_url)
        print("Saving URLS")
        time.sleep(.01)
        print("CHECKING FOR PHRASE")
        phrase_check = check_for_phrase(phrase_to_look_for, soup)
        #times_phrase_found += phrase_check
       # print("Times phrase found: " + str(times_phrase_found))
        if phrase_check > 0:
            file = open("raw_data.txt", "a", encoding="utf-8")
            # time.sleep(.1)
            file.write(str(soup))
            file.close()
            print("RAW DATA SAVED")
            wait(.01)

        time.sleep(.01)
        print("Current url: " + url)
        time.sleep(.01)
        url = fetch_next_url()
        time.sleep(.01)
        try:
            f = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
            page = urllib.request.urlopen(f)
        except:
            # sometimes it just won't load the next url we've chosen, so i'm trying to find ways past that
            # time.sleep(.1)
            f = urllib.request.Request(past_url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
            page = urllib.request.urlopen(f)
        time.sleep(.01)

    except:
        # twitter is not letting me access their site so if we hit something
        # like that, this block should handle that
        # unelegant solution = go to a message board = better chance to find phrase
        url = fetch_next_url()
        print("Can't reach this page, opening a forum")
        f = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        page = urllib.request.urlopen(f)

def check_google(driver,phrase):
    driver.get("https://www.google.com/")
    # identify search box
    m = driver.find_element("name","q")
    # enter search text
    m.send_keys(phrase)
    time.sleep(0.2)
    # perform Google search with Keys.ENTER
    m.send_keys(Keys.ENTER)
    check_page(driver.current_url, driver, phrase)

def wait(seconds):
    time.sleep(seconds)

def fetch_next_url():
    file = open("stripped_urls.txt","r",encoding="utf-8")
    data = file.read().split()
    url = ""
    while url[0:4] != "http":

        print("Incorrect url: "+url)
        url = data[random.randint(0,len(data))]
        time.sleep(.01)
    print("FETCHED URL PROPERLY")
    return url

# eventually need to reform this method to allow for any phrase
def check_for_phrase(phrase,soup):
    if phrase.casefold() in str(soup):
        print("PHRASE FOUND")
        return 1
    print("PHRASE NOT FOUND THIS RUN")
    return 0

def add_to_visited_urls(url):
    visited_file = open("visited_urls.txt", "a",encoding="utf-8")
    visited_file.write(url+"\n")

    visited_file.close()

def get_visited_urls():
    visited_file = open("visited_urls.txt", "r",encoding="utf-8")
    visited_urls = visited_file.read().split()

    visited_file.close()
    return visited_urls

# saving the urls to a file to be used later
def save_urls(soup,driver,past_url):

    visited_urls = get_visited_urls()
    if past_url in visited_urls:
        pass
    else:
        add_to_visited_urls(past_url)
    file = open("stripped_urls.txt", "r+",encoding="utf-8")
    now = datetime.now()
    urls = file.read().split()
    current_time = now.strftime("%H:%M:%S")
    file.write("\n\nNew record added at: " + current_time + "  |  On page "+ driver.title +"\n"+past_url+"\n\n")

    for link in soup.find_all('a'):

        if link != None:
            try:
                # only send it to the file if it actually starts with http because we can almost always assume that will
                # be a link, not perfect though
                if str(link.get('href')[0:4]) == "http" and str(link.get('href')) not in urls:
                    print(link.get('href'))
                    if not str(link.get('href')) in visited_urls:
                        file.write(str(link.get('href')) + "\n")
                    else:
                        print("This url already visted")
            except:
                pass
    file.close()
    #time.sleep(.1)


main()