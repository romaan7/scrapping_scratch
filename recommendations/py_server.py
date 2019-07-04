from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
from io import BytesIO
import urllib.request, json 

def get_user_followers(username):
	with urllib.request.urlopen("https://api.scratch.mit.edu/users/"+username+"/followers") as url:
		data = json.loads(url.read().decode())
		return data
		
def get_user_favriots(username):
	with urllib.request.urlopen("https://api.scratch.mit.edu/users/"+username+"/favorites") as url:
		data = json.loads(url.read().decode())
		return data

def get_user_project(username):
	with urllib.request.urlopen("https://api.scratch.mit.edu/users/"+username+"/projects") as url:
		data = json.loads(url.read().decode())
		return data


def get_recommended_projects(username):
	all_followers = get_user_followers(username)
	all_recommendation=[]
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

	print(all_recommendation)
	return json.dumps(all_recommendation)
	

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
	def end_headers (self):
		#Required for running locally on chrome
		self.send_header('Access-Control-Allow-Origin', '*')
		BaseHTTPRequestHandler.end_headers(self)

	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		query_components = parse_qs(urlparse(self.path).query)
		username = query_components["username"][0]
		response = BytesIO()
		response.write(b'The username recived in URL is ')
		response.write(bytes(username, 'utf-8'))
		self.wfile.write(bytes(get_recommended_projects(username), 'utf-8'))

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
		httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
		print('Started httpserver on port 8000')
		httpd.serve_forever()

	except KeyboardInterrupt:
		print( '^C received, shutting down the web server')
		httpd.socket.close()
	
	
