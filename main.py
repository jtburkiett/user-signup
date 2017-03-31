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
errors =
    "<span class='error'>That's not a valid username</span>"

form= """
        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="" required>
                        "{0}"
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" value="" required>
                        <span class="error" value=""></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" value="" required>
                        <span class="error" value=""></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="">
                        <span class="error"></span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>


""".format(errors)

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
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

class MainHandler(webapp2.RequestHandler):

    def get(self):

        error = self.request.get("error")
        if error:
            error_esc = cgi.escape(error, quote=True)
            error =  error_esc
        else:
            error = ""

        # combine all the pieces to build the content of our response

        content = page_header + form + page_footer
        self.response.write(content)


    def post(self):

        username = self.request.get('username')

        if not valid_username(username):
            error = "{0}".format(errors)
            self.redirect("/?error=", error)











app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
