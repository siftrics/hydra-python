# Copyright © 2020 Siftrics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__version__ = '1.2.0'

import base64
import requests
import time

def _getOrElse(json, key):
    if key not in json:
        raise Exception('This should never happen. Got successful HTTP status code (200) but the body was not the JSON we were expecting.')
    return json[key]

class Client:
    def __init__(self, api_key):
        self.api_key = api_key

    def recognizePayload(self, data_source_id, payload):
        response = requests.post(
            'https://siftrics.com/api/hydra/{}/'.format(data_source_id),
            headers={ 'Authorization': 'Basic {}'.format(self.api_key) },
            json=payload,
        )
        response.raise_for_status()
        json = response.json()
        if 'Rows' not in json:
            raise Exception('This should never happen. '+\
                            'Got successful HTTP status code (200) but '+\
                            'the body was not the JSON we were expecting.')
        return json['Rows']

    def recognize(self, data_source_id, files,
                  doFaster=False,
                  returnTransformedImages=False,
                  returnJpgs=False, jpgQuality=85):
        if type(jpgQuality) is not int:
            raise TypeError('jpgQuality must be an integer')
        if jpgQuality < 1 or jpgQuality > 100:
            raise Exception('jpgQuality must be an integer between 1 and 100 inclusive')
        if type(files) is not list:
            msg = 'You must pass in a list of files, not a {}'.format(type(files))
            raise TypeError(msg)
        payload = { 'files': [],
                    'doFaster': doFaster,
                    'returnTransformedImages': returnTransformedImages,
                    'returnJpgs': returnJpgs,
                    'jpgQuality': jpgQuality }
        for f in files:
            fn = f.lower()
            if fn.endswith('.pdf'):
                mimeType = 'application/pdf'
            elif fn.endswith('.bmp'):
                mimeType = 'image/bmp'
            elif fn.endswith('.gif'):
                mimeType = 'image/gif'
            elif fn.endswith('.jpeg'):
                mimeType = 'image/jpeg'
            elif fn.endswith('.jpg'):
                mimeType = 'image/jpg'
            elif fn.endswith('.png'):
                mimeType = 'image/png'
            else:
                msg = '{} does not have a valid extension; it must be one of '.format(f)+\
                    '".pdf", ".bmp", ".gif", ".jpeg", ".jpg", or ".png".'
                raise Exception(msg)
            with open(f, 'rb') as fileObj:
                base64File = base64.b64encode(fileObj.read())
            payload['files'].append({
                'mimeType': mimeType,
                'base64File': base64File.decode('utf-8'),
            })
        return self.recognizePayload(data_source_id, payload)

    def recognizeBase64(self, data_source_id, base64Files,
                        doFaster=False,
                        returnTransformedImages=False,
                        returnJpgs=False, jpgQuality=85):
        if type(jpgQuality) is not int:
            raise TypeError('jpgQuality must be an integer')
        if jpgQuality < 1 or jpgQuality > 100:
            raise Exception('jpgQuality must be an integer between 1 and 100 inclusive')
        if type(base64Files) is not list:
            msg = 'You must pass in a list of dicts, not a {}'.format(type(files))
            raise TypeError(msg)
        payload = { 'files': base64Files,
                    'doFaster': doFaster,
                    'returnTransformedImages': returnTransformedImages,
                    'returnJpgs': returnJpgs,
                    'jpgQuality': jpgQuality }
        for i, f in enumerate(payload['files']):
            if type(f) is not dict:
                msg = 'You must pass in a list of dicts but '+\
                    'the element at index {} is of type {}'.format(i, type(f))
                raise TypeError(msg)
            if 'mimeType' not in f or 'base64File' not in f:
                raise Exception('Expected each element of base64Files to be '+\
                                'a dict containing "mimeType" and "base64File" field but '+\
                                'the element at index {} does not. '.format(i)+\
                                'Correct example: '+\
                                '{ "mimeType": "image/jpg", "base64File": "..." }')
            if type(f['mimeType']) is not str:
                raise TypeError('Expected the "mimeType" field of each element to be of type str.')
            if type(f['base64File']) is not str:
                raise TypeError('Expected the "base64File" field of each element to be of type str.')
            if f['mimeType'] not in [
                    'application/pdf',
                    'image/bmp',
                    'image/gif',
                    'image/jpeg',
                    'image/jpg',
                    'image/png',
            ]:
                raise Exception('Expected mimeType to be one of '+\
                                '"application/pdf", "image/bmp", "image/gif", '+\
                                '"image/jpeg", "image/jpg", or "image/png" but '+\
                                'the element at index {} has mimeType "{}"'.format(i, f['mimeType']))
        return self.recognizePayload(data_source_id, payload)
