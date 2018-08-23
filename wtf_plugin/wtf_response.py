#################################################################################
#                                                                               #
# Copyright 2018/08/16 Zachary Priddy (me@zpriddy.com) https://zpriddy.com      #
#                                                                               #
# Licensed under the Apache License, Version 2.0 (the "License");               #
# you may not use this file except in compliance with the License.              #
# You may obtain a copy of the License at                                       #
#                                                                               #
# http://www.apache.org/licenses/LICENSE-2.0                                    #
#                                                                               #
# Unless required by applicable law or agreed to in writing, software           #
# distributed under the License is distributed on an "AS IS" BASIS,             #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.      #
# See the License for the specific language governing permissions and           #
# limitations under the License.                                                #
#                                                                               #
#################################################################################


class WTFResponse(object):
    def __init__(self, pid, result, confidence, errors=[], notes=[], function_name='unknown', success=None, **kwargs):
        self._pid = pid
        self._result = result
        self._confidence = confidence
        self._errors = errors
        self._notes = notes
        self._function = function_name
        self._success = success

    def add_error(self, error_message):
        self._errors.append(error_message)

    def add_note(self, note):
        self._notes.append(note)

    @property
    def response(self):
        return {
            'result':     self._result,
            'confidence': self._confidence,
            'errors':     self._errors,
            'notes':      self._notes,
            'pid':        self._pid,
            'function':   self._function,
            'success':    self._success
        }

    @property
    def value(self):
        return self._result

    @property
    def success(self):
        return self._success
