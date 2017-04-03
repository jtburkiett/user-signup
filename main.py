#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re
import cgi

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Signup</h1>
"""


form= """
        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="%(username)s" required>
                        <span class="error" value="" style ="color: red">%(user_error)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" value="" required>
                        <span class="error" value="" style ="color: red">%(pass_error)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" value="" required>
                        <span class="error" value="" style ="color: red">%(ver_error)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="text" value="%(email)s">
                        <span class="error" value="" style ="color: red">%(email_error)s</span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>


"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

welcome = """
<!DOCTYPE html>
<html>
<head>
    <title>Welcome!</title>

</head>
<body>
    <h1>Welcome!</h1>
"""


UNR = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and UNR.match(username)

PWR = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PWR.match(password)

EMR = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return not email or EMR.match(email)

content = page_header + form + page_footer

class MainHandler(webapp2.RequestHandler):

    def write_form(self, username='', user_error='', pass_error='', ver_error='', email='', email_error=''):

        self.response.write(content % { "username": username,
                                        "user_error": user_error,
                                        "pass_error": pass_error,
                                        "ver_error": ver_error,
                                        "email": email,
                                        "email_error": email_error})
    def get(self):

        self.write_form()


    def post(self):

        has_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')


        if not valid_username(username):
            user_error = "Please enter a valid username."
            has_error = True
        else:
            user_error = ""


        if not valid_password(password):
            pass_error = "Please enter a valid password."
            has_error = True
        else:
            pass_error = ""

        if password != verify:
                ver_error = "Your passwords did not match."
                has_error = True
        else:
            ver_error = ""



        if valid_email(email) is not True:
            email_error = "That is not a valid email."
            has_error = True
        else:
            email_error = ""


        if has_error:
            self.write_form(username, user_error, pass_error, ver_error, email, email_error)
        else:
            self.response.out.write("<h1>Welcome " + username + "!!</h1>")















app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
