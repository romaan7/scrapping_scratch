#!/usr/bin/python
#
# Created on Sat Jul 4 20:31:00 2019
# Copyright (C) 2019, shaikhr@tcd.ie
# @author: shaikhr
#
# API reference guide :https://github.com/LLK/scratch-rest-api/wiki/Projects

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
from io import BytesIO
import urllib.request, json 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


#Returns a list of the users that the specified user has followed.
def get_user_following(username):
	with urllib.request.urlopen("https://api.scratch.mit.edu/users/"+username+"/following") as url:
		data = json.loads(url.read().decode())
		return data

#Returns an array of details regarding the projects that a given user has favourited on the website.
def get_user_favriots(username):
	with urllib.request.urlopen("https://api.scratch.mit.edu/users/"+username+"/favorites") as url:
		data = json.loads(url.read().decode())
		return data

#Returns an array with information regarding the projects that a given user has shared on the Scratch website.
def get_user_project(username):
	with urllib.request.urlopen("https://api.scratch.mit.edu/users/"+username+"/projects") as url:
		data = json.loads(url.read().decode())
		return data

#Returns an array with information regarding the project with provided ID of particular username (dosent work , requires auth)
def get_user_project_details(username,project_id):
	with urllib.request.urlopen("https://api.scratch.mit.edu/users/"+username+"/projects/"+project_id) as url:
		data = json.loads(url.read().decode())
		return data

# ( No working API, therefor using lxml html parsing)
def get_author_from_project(project_id):
	url = 'https://scratch.mit.edu/projects/'+str(project_id)
	#rendered page is a JS script, no use of lxml #alternative is using selenium
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome('./selenium/chromedriver.exe',chrome_options=chrome_options)  # Optional argument, if not specified will search path.
	#driver = webdriver.Chrome('./selenium/chromedriver.exe')
	driver.get(url)
	time.sleep(5)
	author = driver.find_element_by_xpath("//div[@class='title']/a").text
	driver.quit()
	return author
	
#Generates recommendations for a given username, and returns a json object
def get_recommended_projects(username):
	all_followers = get_user_following(username)
	all_recommendation=[]

	
	#Get details of the users who the user is following ( projects of following , favorites of following)
	for user in all_followers:
		all_projects = get_user_project(user["username"])
		for project in all_projects:
			recommendations={}
			recommendations['id'] = project["id"]
			recommendations['title'] = project["title"]
			recommendations['stats'] = project["stats"]
			recommendations['score'] = 0
			for s in project["stats"]:
				recommendations['score'] += project["stats"][s]
			all_recommendation.append(recommendations)
			recommendations['reason'] = user["username"]
			recommendations['reason_id'] = user["id"]
			
		all_followers_favourite = get_user_favriots(user["username"])
		for favourite in all_followers_favourite:
			recommendations={}
			recommendations['id']= favourite["id"]
			recommendations['title']= favourite["title"]
			recommendations['stats'] = project["stats"]
			recommendations['score'] = 0
			for s in project["stats"]:
				recommendations['score'] += project["stats"][s]		
			all_recommendation.append(recommendations)
			recommendations['reason'] = user["username"]
			recommendations['reason_id'] = user["id"]
	
	#Get details of the favorite project of the user ( No working API, therefor using selenium for parsing).
	#Too slow needs,an alternative
	all_favriots = get_user_favriots(username)
	for favriots in all_favriots:
		project_id = favriots["id"]
		#get_author_from_project(project_id)	
		
	print(all_recommendation)
	return json.dumps(all_recommendation)
	
#Extends pythons simple http server to handle GET requests locally
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
	def end_headers (self):
		#Required for running locally on chrome ( allows CORS for all request to the server )
		self.send_header('Access-Control-Allow-Origin', '*')
		BaseHTTPRequestHandler.end_headers(self)
	
	#Gets the username in the GET request url as username and returns a list of recommendations
	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		query_components = parse_qs(urlparse(self.path).query)
		username = query_components["username"][0]
		response = BytesIO()
		response.write(b'The username recived in URL is ')
		response.write(bytes(username, 'utf-8'))
		self.wfile.write(bytes(get_recommended_projects(username), 'utf-8'))
	
	#Handels post request, wrote this to get data via POST, not used currently
	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		body = self.rfile.read(content_length)
		self.send_response(200)
		self.end_headers()
		response = BytesIO()
		response.write(b'This is POST request. ')
		response.write(body)
		self.wfile.write(response.getvalue())
		
if __name__ == "__main__":
	try:
		#NOTE: If you update port here, remember to update in the JS extension as well.
		httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
		print('Started httpserver on port 8000')
		httpd.serve_forever()

	except KeyboardInterrupt:
		print( '^C received, shutting down the web server')
		httpd.socket.close()
	
	
