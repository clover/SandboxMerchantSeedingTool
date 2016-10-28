import webapp2
import faker
from faker import Factory
from webapp2 import WSGIApplication, Route

from google.appengine.api import urlfetch

#ROUTES
class Home(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("hello world")

routes = [
    Route (r'/', handler = Home)
]

app = webapp2.WSGIApplication(routes, debug=True)

def main():
    app.run()

if __name__ == "__main__":
    main()
