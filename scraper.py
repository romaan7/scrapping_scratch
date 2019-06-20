# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 16:36:50 2019

@author: shaikhr
"""

import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import csv
import json



#Excepts a list of urls for user's following page, goes to each URL and gets records of the followers
def traverse_page(pages):
    with open('users.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["user_name"],total_following)
        for page in pages:
            response = requests.get(page)
            soup = BeautifulSoup(response.text, "html.parser")
            all_links = soup.findAll('a')
            for link in all_links:
                try:
                    link = link['href']
                    if re.match("^/users", link):
                        user_name = link.replace("/users/","").replace("/","")
                        csv_writer.writerow([user_name])
                except:
                    pass

#https://api.scratch.mit.edu/users/I_FoLoww_ALL/following?limit=40&offset=1000
#response = requests.get(api_base_url+user_url+user_name_url+following_url+"?limit=40&offset="+offset)
#following = json.loads(response.text)

def access_api():
    for offset in list(range(0,int(total_following[0]),40)):
        response = requests.get(api_base_url+user_url+user_name_url+following_url+"?limit=40&offset="+str(offset))
        following = json.loads(response.text)
        print(following[1]['username']+str(offset))
    
    
def main():
    #Varibles for URLs
    base_url='https://scratch.mit.edu'
    user_url='/users/'
    user_name_url = 'I_FoLoww_ALL'
    following_url='/following/'
    api_base_url='https://api.scratch.mit.edu'

    seed_url = base_url+user_url+user_name_url+following_url

    #Originil URL format should be like below
    #seed_url = 'https://scratch.mit.edu/users/I_FoLoww_ALL/following/'

    #Call and parse the HTML of the user page
    response = requests.get(seed_url)
    soup = BeautifulSoup(response.text, "html.parser")

    #Find all the anchor tags on the page
    all_links = soup.findAll('a')
    all_headings = soup.findAll('h2') #Find h2 tags for getting the count of the total followers
    
    pages=[] # Holds the construsted URLs for the following users.
    total_following=0 #Total follower count

    #Get all the URLs for follower page and append to pages list
    for i in all_links:
        try:
            link = i['href']
            if re.match("^\?page=", link):
                pages.append(seed_url+link)
        except:
            pass

    #Get total following count.
    for i in all_headings:
        total_following = re.findall(r'\d+',i.contents[1])

    #traverse_page(pages)
    #access_api()
    
if __name__ == "__main__" :
    main()
    