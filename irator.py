"""
irator
~~~~~~

A Twisted-friendly interface to IRE's Irator API

IRE's Irator Documentation: http://www.ironrealms.com/IREAPIdocumentation.pdf

"""

from twisted.web.client import getPage
from twisted.internet.defer import inlineCallbacks, returnValue
import json
from datetime import datetime
from urllib import urlencode
import requests

endpoint = 'http://api.achaea.com/'

class Unauthorized(Exception):
    pass

class BaseIrator(object):

    def __init__(self, character=None, password=None):
        self.character = character
        self.password = password

    def gamefeed(self, limit=None, id=None):
        params = {}

        if limit:
            params['limit'] = limit

        if id:
            params['id'] = id

        return self._request('gamefeed', params)

    def orglogs(self, org, day=0):

        orglog = self._request('orglogs/' + org.lower(), params={'day': day})

        if orglog == 'Access denied':
            raise Unauthorized('Access denied')

        result = []
        for line in orglog:
            result.append({
                'date': datetime.fromtimestamp(line['date']),
                'event': str(line['event'])
            })

        return result

    def news(self):
        return self._request('news')


class Irator(BaseIrator):

    def characters(self, name=None):
        if name is None:
            response = self._request('characters')
            result = {
                'total': int(response['count']),
                'characters': [str(c['name']) for c in response['characters']]
            }
        else:
            response = self._request('characters/' + name)
            result = response

        return result

    def news_section(self, section, page=1):
        pass

    def news_article(self, section, article):
        pass

    def _request(self, resource, params={}):
        resource += '.json'

        if self.character and self.password:
            params.update({
                'character': self.character,
                'password': self.password
            })

        r = requests.get(endpoint + resource, params=params)

        return r.json()


class TwistedIrator(BaseIrator):

    params = {
        'agent': 'Irator API Client',
        'method': 'GET',
    }

    @inlineCallbacks
    def characters(self, name=None):
        if name is None:
            response = yield self._request('characters')
            result = {
                'total': int(response['count']),
                'characters': [str(c['name']) for c in response['characters']]
            }
        else:
            response = yield self._request('characters/' + name)
            result = response

        returnValue(result)

    @inlineCallbacks
    def news_section(self, section, page=1):
        response = yield self._request('news/%s' % section.lower())
        returnValue(NewsSection(response, self))

    @inlineCallbacks
    def news_article(self, section, article):
        response = yield self._request('news/%s/%s' % (section.lower(), article))
        returnValue(NewsArticle(response, self))

    def gamefeed(self, limit=None, id=None):
        params = {}

        if limit:
            params['limit'] = limit

        if id:
            params['id'] = id

        return self._request('gamefeed', params)

    @inlineCallbacks
    def orglogs(self, org=None, day=0):
        result = super(TwistedIrator, self).orglogs(org=org, day=day)

        returnValue(result)

    @inlineCallbacks
    def _request(self, resource, params={}):

        resource += '.json'

        if self.character and self.password:
            params.update({
                'character': self.character,
                'password': self.password
            })

        if len(params) > 0:
            resource = resource + "?" + urlencode(params)

        response = yield getPage(endpoint + resource, headers=self.params)

        returnValue(json.loads(response))


class NewsSection(list):

    def __init__(self, section, client):
        self.client = client
        news = section['news']
        self._raw = news
        for article in news:
            self.section = article['section']
            self.append({
                'id': article['id'],
                'from': str(article['from']),
                'to': str(article['to']),
                'date': datetime.fromtimestamp(article['date']),
                'subject': str(article['subject'])
            })

    def next(self):
        if self._raw['next'] is False:
            return None

        page = self._get_page(self._raw['next'])
        return self.client.news_section(self.section, page=page)

    def previous(self):
        if self._raw['previous'] is False:
            return None

        page = self._get_page(self._raw['previous'])
        return self.client.news_section(self.section, page=page)

    def _get_page(self, url):
        index = url.index('page=')
        return int(url[index + 5:])


class NewsArticle(object):

    def __init__(self, article, client):
        self.client = client
        post = article['post']
        self.id = post['id']
        self.subject = post['subject']
        self.author = str(post['from'])
        self.section = str(post['section'])
        self.to = str(post['to'])
        self.date = datetime.fromtimestamp(post['date'])
        self.date_ingame = str(post['date_ingame'])
        self.message = post['message']

    def next(self):
        return self.client.news(self.section, self.id + 1)

    def previous(self):
        return self.client.news(self.section, self.id - 1)
