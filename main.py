import webapp2
import cgi
import re


form = """
        <body>
            <h1> Signup </h1>
            <form method= "post" >
                <table>
                    <tr>
                        <td>
                            <label>Username</label>
                        </td>
                        <td>
                            <input type= "text" name= "username" value= "%(username)s"/>
                        </td>
                        <td style="color: red">
                            %(invalid_username)s
                        <td>
                    </tr>
                    <tr>
                        <td>
                            <label>Password</label>
                        </td>
                        <td>
                            <input type= "password" name= "password" value=""/>
                        </td>
                        <td style="color: red">
                            %(invalid_password)s
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label>Verify Password</label>
                        </td>
                        <td>
                            <input type= "password" name= "verify" value=""/>
                        </td>
                        <td style="color: red">
                            %(invalid_verify)s
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label>Email (optional)</label>
                        </td>
                        <td>
                            <input type= "text" name= "email" value="%(email)s"/>
                        </td>
                        <td style="color: red">
                            %(invalid_email)s
                        </td>
                    </tr>
                </table>
                <input type="submit"/>
            </form>
        </body>
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


class Signup(webapp2.RequestHandler):

    def write_form(self, username="",email="", invalid_username="",invalid_password="",invalid_verify="",invalid_email=""):
                    
        self.response.write(form % {"username":username,"email": email,
                                    "invalid_username": invalid_username,
                                    "invalid_password": invalid_password,
                                    "invalid_verify": invalid_verify,
                                    "invalid_email": invalid_email})
    
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
        
        escape_username = cgi.escape(username, quote=True)
        escape_password = cgi.escape(password, quote=True)
        escape_verify = cgi.escape(verify, quote=True)
        escape_email = cgi.escape(email, quote=True)

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
            self.write_form(username, email, invalid_username, invalid_password, invalid_verify, invalid_email)
        else:
            self.redirect('/welcome?username=' + username)



class Welcome(webapp2.RequestHandler):
    def get(self):
        welcome_message = "Welcome, "
        username = self.request.get("username")
        self.response.write("<h1>" + welcome_message + username +"</h1>" )
        

       
app = webapp2.WSGIApplication([
    ('/', Signup), ('/welcome', Welcome)
], debug=True)
