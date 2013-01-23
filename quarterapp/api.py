#
#  Copyright (c) 2013 Markus Eliasson, http://www.quarterapp.com/
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
import sys
import os
import json

import tornado.web
import tornado.escape
from tornado.options import options

from quarterapp.basehandlers import *
from quarterapp.storage import *
from quarterapp.errors import *
from quarterapp.utils import *

class ActivityApiHandler(AuthenticatedHandler):
    """
    The activity API handler implements all supported operations on activities.
    """
    @authenticated_user
    def get(self):
        """
        Get the complete list of activities
        """
        user = self.get_current_user()
        activities = get_activities(self.application.db, user["id"])
        if not activities:
            activities = []
        self.write( { "activities" : activities } )
        self.finish()

    @authenticated_user
    def post(self):
        """
        Create a new activity
        """
        title = self.get_argument("title2", "")
        color = self.get_argument("color2", "")

        errors = []

        if not title or len(title) == 0:
            errors.append( ERROR_NO_ACTIVITY_TITLE )
        if not color or len(color) == 0:
            errors.append( ERROR_NO_ACTIVITY_COLOR )
        if not valid_color_hex(color):
            errors.append( ERROR_NOT_VALID_COLOR_HEX )
        
        if len(errors) > 0:
            self.respond_with_errors(errors)
        else:
            user = self.get_current_user()
            add_activity(self.application.db, user["id"], title, color)
            self.write_success()

    @authenticated_user
    def put(self, activity_id):
        """
        Update a given activity
        """
        pass

    @authenticated_user
    def delete(self, activity_id):
        """
        Delete a given activity
        """
        pass