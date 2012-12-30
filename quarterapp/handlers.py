#
#  Copyright (c) 2012 Markus Eliasson, http://www.quarterapp.com/
#
#  Permission is hereby granted, free of charge, to any person obtaining
#  a copy of this software and associated documentation files (the
#  "Software"), to deal in the Software without restriction, including
#  without limitation the rights to use, copy, modify, merge, publish,
#  distribute, sublicense, and/or sell copies of the Software, and to
#  permit persons to whom the Software is furnished to do so, subject to
#  the following conditions:
#
#  The above copyright notice and this permission notice shall be
#  included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
#  LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
#  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import logging
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def write_success(self):
        self.write({
            "error" : SUCCESS,
            "message" :"Ok"})
        self.finish()

    def write_error(self, error_code, error_message):
        self.write({
            "error" : error_code,
            "message" : error_message})
        self.finish()

    def write_unauthenticated_error(self):
        self.write({
            "error" : ERROR_NOT_AUTHENTICATED,
            "message" :"Not logged in"})
        self.finish()


class AuthenticatedHandler(BaseHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json:
            return None
        return tornado.escape.json_decode(user_json)


class ProtectedStaticHandler(tornado.web.StaticFileHandler):
    """
    Handle static files that are protected.
    """
    @tornado.web.authenticated
    def get(self, path, include_body=True):
        super(tornado.web.StaticFileHandler, self.get(path, include_body))


class SettingsHandler(BaseHandler):
    """Used as the HTTP API to retrieve and update application settings.
    User must be authenticated as administrator to be able to use
    """
    def get(self, key):
        def local_error():
            logging.warning("Could not retrieve setting (%s)", key)
            self.write_error(1001, "Could not retrieve setting")

        try:
            if key:
                value = self.application.quarter_settings.get_value(key)
                if value:
                    self.write({"key" : key, "value" : value})
                    self.finish()
                else:
                    local_error()
            else:
                local_error()
        except:
            local_error()

    def post(self, key):
        def local_error():
            logging.warning("Trying to set setting (%s) without a given value", key)
            self.write_error(1002, "No value specified")

        try:
            if key:
                value = self.get_argument("value", "")
                self.application.quarter_settings.put_value(key, value)
                self.write({"key" : key, "value" : value})
                self.finish()
            else:
                local_error()
        except:
            local_error()

class AdminDefaultHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(u"admin/general.html")


class AdminUsersHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(u"admin/users.html")


class AdminNewUserHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(u"admin/new-user.html")


class AdminStatisticsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(u"admin/statistics.html")


class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(u"/")


class SignupHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(u"signup.html")


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(u"login.html")


class HeartbeatHandler(tornado.web.RequestHandler):
    """
    Heartbeat timer, just echo server health
    """
    def get(self):
        self.write("beat");