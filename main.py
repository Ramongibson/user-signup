import webapp2
import cgi
import re


form = """<h1> Sign Up </h1><form method= "post" >
        <strong><label>Username</label><input type= "text" name= "username" value= "%(username)s"/><div style="color: red">%(invalid_username)s</div><br>
        <label>Password</label><input type= "password" name= "password" value=""/><div style="color: red">%(invalid_password)s</div><br>
        <label>Verify Password</label><input type= "password" name= "verify" value=""/><div style="color: red">%(invalid_verify)s</div><br>
        <label>Email(optional)</label><input type= "text" name= "email" value="%(email)s"/><div style="color: red">%(invalid_email)s</div><br></strong>
        <input type="submit"/></form>
        """

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)


class MainPage(webapp2.RequestHandler):

    def write_form(self, username="",email="", invalid_username="",invalid_password="",invalid_verify="",invalid_email=""):
                    
        self.response.write(form % {"username":username,"email": email,
                                    "invalid_username": invalid_username,
                                    "invalid_password": invalid_password,
                                    "invalid_verify":invalid_verify,
                                    "invalid_email":invalid_email})
    
    def get(self):
        self.write_form()

    def post(self):
        error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        invalid_username = ""
        invalid_password = ""
        invalid_verify = ""
        invalid_email = ""

        replace = dict(username = username, email = email)
        if not valid_username(username):
            invalid_username = "Username is not valid."
            error = True

        if not valid_password(password):
            invalid_password= " Please enter a valid password."
            error = True
        elif password != verify:
            invalid_verify = "Passwords doesn't match."
            error = True

        if not valid_email(email):
            invalid_email = "Please enter a valid email address."
            error = True

        if error:
            self.write_form(username,email,invalid_username,invalid_password,invalid_verify,invalid_email)
        else:
            self.redirect('/welcome?username=' + username)



class Welcome(webapp2.RequestHandler):
    def get(self):
        welcome_message = "Welcome, "
        username = self.request.get("username")
        self.response.write("<h1>" + welcome_message + username +"</h1>" )
        

       




app = webapp2.WSGIApplication([
    ('/', MainPage), ('/welcome', Welcome)
], debug=True)
