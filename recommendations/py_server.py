#!/usr/bin/python
#
# Created on Sat Jul 4 20:31:00 2019
# Copyright (C) 2019, shaikhr@tcd.ie
# @author: shaikhr
#
# API reference guide : https://github.com/LLK/scratch-rest-api/wiki/Projects
# Scratch data guide  : https://communitydata.science/scratch-data/

#Libs for Serving
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
from io import BytesIO
import urllib.request, json 

#not required for now can be commented
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

#Libs for data analysis
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn import preprocessing
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import correlation


#Returns a list of the users that the specified user has followed.
def get_user_following(username, LIMIT):
	if not LIMIT:
		LIMIT = 10
	OFFSET = 0
	with urllib.request.urlopen("https://api.scratch.mit.edu/users/"+username+"/following?limit="+str(LIMIT)+"&offset="+str(OFFSET)) as url:
		data = json.loads(url.read().decode())
		return data

		
#Returns an array of details regarding the projects that a given user has favourited on the website.
def get_user_favriots(username, LIMIT):
	if not LIMIT:
		LIMIT = 3
	OFFSET = 0
	with urllib.request.urlopen("https://api.scratch.mit.edu/users/"+username+"/favorites?limit="+str(LIMIT)+"&offset="+str(OFFSET)) as url:
		data = json.loads(url.read().decode())
		return data

		
#Returns an array with information regarding the projects that a given user has shared on the Scratch website.
def get_user_projects(username, LIMIT):
	if not LIMIT:
		LIMIT = 10
	OFFSET = 0
	with urllib.request.urlopen("https://api.scratch.mit.edu/users/"+username+"/projects?limit="+str(LIMIT)+"&offset="+str(OFFSET)) as url:
		data = json.loads(url.read().decode())
		return data

		
#Returns an array with information regarding the project with provided ID of particular username (dosent work , requires auth)
def get_user_project_details(username,project_id):
	with urllib.request.urlopen("https://api.scratch.mit.edu/users/"+username+"/projects/"+project_id) as url:
		data = json.loads(url.read().decode())
		return data

		
#Gets the project name from given project ID (api deprecated , using selenium to render JS)
def get_project_title(project_id):
	url = 'https://scratch.mit.edu/projects/'+str(project_id)
	#rendered page is a JS script, no use of lxml #alternative is using selenium
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome('./selenium/chromedriver.exe',chrome_options=chrome_options)  # Optional argument, if not specified will search path.
	#driver = webdriver.Chrome('./selenium/chromedriver.exe')
	driver.get(url)
	time.sleep(5)
	title = driver.title
	driver.quit()
	return title


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

	
#Takes project json object as input and returns the stats if present.
def get_project_stats(project_obj):
	#Difficult to retrive the below values from current APIs therefor assigning mock values.
	sprites_website = 5
	scripts_website = 10
	blocks = 6 
	block_types = 7
	images = 2
	sounds = 2 
	ugstrings = 11
	stats = {'sprites_website':sprites_website,'scripts_website':scripts_website,'blocks':blocks,'block_types':block_types,'images':images,'sounds':sounds,'ugstrings':ugstrings}
	for key in project_obj:
		if key == 'id':
			stats['id'] = project_obj[key]
		if key == 'stats':
			stats.update(project_obj[key])
			return stats
	return stats

	
#Checks if the supplied project has a remix associated with it. If yes returns the remix object containing the remixes 
def is_project_remix(project_obj):
	for key in project_obj:
		if key == 'remix':
			#Nested for not too heavy because only 2 remix has only two components
			for x in project_obj[key]:
				if project_obj[key][x] != None:
					return project_obj[key]
				else:
					return False


#Gets from the CSV database against the supplies stats of the project
def generate_recommmendation_from_db(stats_obj):
	#Load data from the csv
	projects_df = pd.read_csv('data/CSVs/projects.csv', sep=',',index_col=0, nrows=100)
	#index = projects_df.index
	#columns = projects_df.columns
	#values = projects_df.values
	
	#Filter columns 
	required_columns_df = projects_df[['viewers_website','lovers_website','downloaders_website','sprites_website','scripts_website', 'blocks', 'block_types', 'images', 'sounds', 'ugstrings']]
	
	project_id = stats_obj.pop('id')
	
	new_stats_row = pd.Series(stats_obj)
	new_stats_row.name = project_id
	required_columns_df = required_columns_df.append(new_stats_row)
	
	#Impute the missing values using IterativeImputer from sklearn
	#imp = SimpleImputer(missing_values=np.nan, strategy='mean')
	imp = IterativeImputer(max_iter=10,initial_strategy='most_frequent', random_state=0)
	imputed_DF = pd.DataFrame(imp.fit_transform(required_columns_df))
	imputed_DF.columns = required_columns_df.columns
	imputed_DF.index = required_columns_df.index
	
	#Normalize the data for further calculation
	x = imputed_DF.values
	min_max_scaler = preprocessing.MinMaxScaler()
	x_scaled = min_max_scaler.fit_transform(imputed_DF)
	normalised_df = pd.DataFrame(x_scaled)
	normalised_df.columns = required_columns_df.columns
	normalised_df.index = required_columns_df.index
	
	#Calculate the RMSE score
	normalised_df['RMSE'] = pd.Series((normalised_df.iloc[:,1:]**2).sum(1).pow(1/2))
	print(normalised_df)

	#Generate the similarity matrix based on the the new project stats.
	sim = cosine_similarity(normalised_df)
	final_df = pd.DataFrame(sim)
	final_df.columns = required_columns_df.index
	final_df.index = required_columns_df.index	
	print(final_df)

	#Get Top 5 from the similarity matrix 
	top5 = final_df.loc[project_id].nlargest(5)
	recommendation_pairs = top5.to_dict()
	
	return recommendation_pairs

	
#Calculates recommendation score by taking the mean of the generated recommendation matrix based on provided input stats of the project.
#Need more optimized method to calculate more accurate score. Currently needs work.( Probably apply K nearest neighbor technique to get nearest neighbor and calculate further score.
def calculate_recommendation_score(stats_obj):
	MAX_ITER = 10
	RECOMMENDATION_NUMBER = 5
	projects_df = pd.read_csv('data/CSVs/projects.csv', sep=',',index_col=0, nrows=100)
	
	#Filter columns 
	required_columns_df = projects_df[['viewers_website','lovers_website','downloaders_website','sprites_website','scripts_website', 'blocks', 'block_types', 'images', 'sounds', 'ugstrings']]
	
	#project_id = stats_obj.pop('id')
	project_id = '10000001'
	
	new_stats_row = pd.Series(stats_obj)
	new_stats_row.name = project_id
	required_columns_df = required_columns_df.append(new_stats_row)
	
	#Impute the missing values using IterativeImputer from sklearn
	#imp = SimpleImputer(missing_values=np.nan, strategy='mean')
	imp = IterativeImputer(max_iter=MAX_ITER,initial_strategy='most_frequent', random_state=0)
	imputed_DF = pd.DataFrame(imp.fit_transform(required_columns_df))
	imputed_DF.columns = required_columns_df.columns
	imputed_DF.index = required_columns_df.index
	
	#Normalize the data for further calculation
	x = imputed_DF.values
	min_max_scaler = preprocessing.MinMaxScaler()
	x_scaled = min_max_scaler.fit_transform(imputed_DF)
	normalised_df = pd.DataFrame(x_scaled)
	normalised_df.columns = required_columns_df.columns
	normalised_df.index = required_columns_df.index
	
	#Calculate the RMSE score
	normalised_df['RMSE'] = pd.Series((normalised_df.iloc[:,1:]**2).sum(1).pow(1/2))

	#Generate the similarity matrix based on the the new project stats.
	sim = cosine_similarity(normalised_df)
	final_df = pd.DataFrame(sim)
	final_df.columns = required_columns_df.index
	final_df.index = required_columns_df.index	

	score = final_df.loc[project_id].nlargest(RECOMMENDATION_NUMBER)
	final_score = 0
	for x in score:
		final_score += x

	return final_score/RECOMMENDATION_NUMBER

	
#Reformats the stats object in the format required for the recommendation method
#DICT FORMAT: {'sprites_website': int64(xxx), 'scripts_website': int64(xxx), 'blocks': int64(xxx), 'block_types': int64(xxx), 'images': int64(xxx), 'sounds': int64(xxx), 'ugstrings': int64(xxx), 'viewers_website': int64(xxx), 'lovers_website': int64(xxx), 'downloaders_website': int64(xxx)}
def reformat_stats(stats_obj):
	stats_obj['viewers_website'] = stats_obj.pop('views')
	stats_obj['lovers_website'] = stats_obj.pop('loves')
	stats_obj['downloaders_website'] = stats_obj.pop('favorites') #Need to fix this
	stats_obj.pop('comments') 
	stats_obj.pop('remixes')
	return stats_obj
	
	
#Generates recommendations for a given username, and returns a json object
def get_recommended_projects(username):
	RECOMMENDATION_REASON_1 = "<i> Recommended because you follow: <a  href=/users/"
	RECOMMENDATION_REASON_2 = "<i> Recommended because you have project: <a  href=/projects/"
	RECOMMENDATION_REASON_3 = "<i> Recommended because user: <a  href=/projects/"
	RECOMMENDATION_REASON_4 = "<i> Recommended because its a remix of <a  href=/projects/"

	all_followers = get_user_following(username,10)
	all_recommendation = []

	#Gets recommendation from the csv database against the given user data
	for projects in get_user_projects(username,5):
		project_stats = get_project_stats(projects)
		project_id = project_stats["id"]

		recommendations_from_db = generate_recommmendation_from_db(reformat_stats(project_stats))
		recommended_project_ids = recommendations_from_db.keys()

		for recom in recommended_project_ids:
			print(get_project_title(recom))
			recommendations={}
			recommendations['id'] = recom
			recommendations['title'] = recom #get_project_title(recom)
			recommendations['stats'] = project_stats
			recommendations['score'] = recommendations_from_db[recom]
			recommendations['reason'] = RECOMMENDATION_REASON_2 + str(project_id) + ">" + str(project_id) + "</a>"
			recommendations['reason_id'] = username
			all_recommendation.append(recommendations)

	#Get details of the users who the user is following ( projects of following , favorites of following)
	for user in all_followers:
		
		#Projects from followers
		all_follower_projects = get_user_projects(user["username"],5)
		for project in all_follower_projects:
			recommendations={}
			recommendations['id'] = project["id"]
			recommendations['title'] = project["title"]
			recommendations['stats'] = project["stats"]
			recommendations['score'] = calculate_recommendation_score(project["stats"])
			recommendations['reason'] = RECOMMENDATION_REASON_1 + user["username"] + ">" + user["username"] + "</a>"
			recommendations['reason_id'] = user["id"]
			all_recommendation.append(recommendations)
		
		#Projects that the followers have liked 
		all_followers_favourite = get_user_favriots(user["username"],5)
		for favourite in all_followers_favourite:
			recommendations={}
			recommendations['id']= favourite["id"]
			recommendations['title']= favourite["title"]
			recommendations['stats'] = favourite["stats"]
			recommendations['score'] = calculate_recommendation_score(favourite["stats"])
			recommendations['reason'] = RECOMMENDATION_REASON_3 + user["username"] + ">" + user["username"] + "</a> has liked it."
			recommendations['reason_id'] = user["id"]
			all_recommendation.append(recommendations)
		
		#Check if project has remix of the project, and add that to the recommendation list.
		for project in get_user_projects(user["username"],5):
			is_remix = is_project_remix(project)
			if is_remix:
				recommendations={}
				recommendations['id']= is_remix["parent"]
				recommendations['title']= project["title"]
				recommendations['stats'] = project["stats"]
				recommendations['score'] = calculate_recommendation_score(project["stats"])
				recommendations['reason'] = RECOMMENDATION_REASON_4 + str(is_remix["root"]) + ">" + str(is_remix["root"]) + "</a>"
				recommendations['reason_id'] = user["id"]
				all_recommendation.append(recommendations)
				
	#Get details of the favorite project of the user ( No working API, therefor using selenium for parsing).
	#Too slow needs,an alternative
	all_favriots = get_user_favriots(username,5)
	for favriots in all_favriots:
		project_id = favriots["id"]
		#get_author_from_project(project_id)	
		
	#print(all_recommendation)
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
		PORT = 8000
		HOST = 'localhost'
		httpd = HTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
		print('Started httpserver on port ' + str(PORT))
		httpd.serve_forever()

	except KeyboardInterrupt:
		print( '^C received, shutting down the web server')
		httpd.socket.close()
