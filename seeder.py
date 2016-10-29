import webapp2
import faker
from faker import Factory
from webapp2 import WSGIApplication, Route

class Home(webapp2.RequestHandler):
    def get(self):
        fake = Factory.create()
        print fake.name()
        print fake.name()
        print fake.name()
        print fake.name()
        print fake.name()
        print fake.name()
        print fake.name()
        print fake.name()
        print fake.name()
        self.response.out.write("hello world")

#ROUTES
routes = [
    Route (r'/', handler = Home)
]

app = webapp2.WSGIApplication(routes, debug=True)

def main():
    app.run()

if __name__ == "__main__":
    main()
