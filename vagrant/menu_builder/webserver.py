from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/restaurant"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				printer = ""
				allRestaurants = session.query(Restaurant).all()
				for restaurant in allRestaurants:
					printer += restaurant.name
					printer += " <a href='/restaurant/%s/edit'>Edit</a> " % restaurant.id
					printer += "<a href='/restaurant/%s/delete'>Delete</a>" % restaurant.id
					printer += "<br>"
					
					
				output = ""
				output += "<html><body>"
				output += "<h1>Would you like to add a new restaurant</h1>"
				output += "<button><a href='/restaurant/add'>Add restaurant</a></button>"
				output += "<br><div> %s" % printer
				output += "</div></body></html>"
				self.wfile.write(output)
				return
			

			if self.path.endswith("/restaurant/add"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>Add a new restaurant:</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action'/restaurant/add'>"
				output += "<input type='text' name='newRestaurant'>"
				output += "<input type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				return

			
			if self.path.endswith("/edit"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				curr_restaurant = session.query(Restaurant).filter_by(id=self.path.split('/')[2]).one()

				output = ""
				output += "<html><body>"
				output += curr_restaurant.name
				output += "<form method='POST' enctype='multipart/form-data' action'/restaurant/%s/edit'>" % curr_restaurant.id
				output += "<input type='text' name='editRestaurant' placeholder='%s'>" % curr_restaurant.name
				output += "<input type='submit' value='Edit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				return
				

			if self.path.endswith("/delete"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				curr_restaurant = session.query(Restaurant).filter_by(id=self.path.split('/')[2]).one()

				output = ""
				output += "<html><body>"
				output += "<h1>Are you sure you would like to delete %s?" % curr_restaurant.name
				output += "<form method='POST' enctype='multipart/form-data' action'/restaurant/%s/delete'>" % curr_restaurant.id
				output += "<input type='submit' name='deleteRestaurant' value='Yes'><a href='/restaurant'><button>No</button></a></form>"
				output += "</body></html>"
				self.wfile.write(output)
				return

		except IOError:
			self.send_error(404, "File not found %s" % self.path)


	def do_POST(self):
		try:
			if self.path.endswith("/restaurant/add"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurant')

				
				newRestaurant = Restaurant(name=messagecontent[0])
				session.add(newRestaurant)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurant')
				self.end_headers()

			if self.path.endswith("/edit"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('editRestaurant')

				curr_restaurant = session.query(Restaurant).filter_by(id=self.path.split('/')[2]).one()
				curr_restaurant.name = messagecontent[0]
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurant')
				self.end_headers()

			if self.path.endswith("/delete"):

				curr_restaurant = session.query(Restaurant).filter_by(id=self.path.split('/')[2]).one()
				session.delete(curr_restaurant)
				session.commit()

				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location', '/restaurant')
				self.end_headers()

		except:
			pass

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print("Web server running on port %s" % port)
		server.serve_forever()
	except KeyboardInterrupt:
		print("C entered, server is stopping...")
		server.socket.close()




if __name__ == '__main__':
	main()