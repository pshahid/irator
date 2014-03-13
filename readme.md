Irator
======

A Twisted-friendly client implementation of IRE's Irator API.

This is designed to work with Sage, which means it is meant to work inside the
Twisted event loop, which of course means it uses Deferreds and callbacks. Yay? Well...anyways...

There's also a class that doesn't require Twisted in the works...

Usage
-----

(If you're not inside a running Twisted reactor, you'll need to start one)

Create a client instance with optional character authorization information:

    from irator import TwistedIrator
    client = TwistedIrator(character='Jaiko', password='sagerawksyersawks')


A basic callback to handle results and print them:

    def print_result(response):
        print(response)


Print a list of characters currently online and visible:

    >>> client.characters().addCallback(print_result)
    {'total': 122, 'characters': ['Achimrst', 'Aeni', 'Ahmet', 'Aisling', 'Alrena', 'Amira', 'Assai', 'Autumn', 'Baratha', 'Besra', 'Bithiah', 'Cathy', 'Chryseas', 'Deinemor', 'Diff', 'Dirgmal', 'Drual', 'Ecclesias', 'Elianon', 'Gartnaich', 'Giulia', 'Goggo', 'Herthenia', 'Iakimen', 'Irontounge', 'Isia', 'Jacintha', 'Janocz', 'Jasaadi', 'Jonesey', 'Josoul', 'Juliet', 'Kaden', 'Kellonius', 'Khaibit', 'Kiden', 'Kitta', 'Kotaru', 'Lerilyth', 'Lis', 'Llyweith', 'Lorath', 'Mawgth', 'Melea', 'Ninlea', 'Nizana', 'Orzaansyn', 'Procelean', 'Quoetzl', 'Sable', 'Safi', 'Scrim', 'Severina', 'Sunia', 'Teghaine', 'Teldrim', 'Terav', 'Terra', 'Tess', 'Tiaramyst', 'Wyverex', 'Zada', 'Zhivago', 'Zincor']}

Get the fullname of a character:

    >>> client.characters('jaiko').addCallback(print_result)
    "Jaiko Rian"

Get all news sections:

    >>> client.news().addCallback(print_result)
    [{u'total': 19293, u'uri': u'http://api.achaea.com/news/public.json', u'name': u'Public'}, {u'total': 3989, u'uri': u'http://api.achaea.com/news/announce.json', u'name': u'Announce'}, {u'total': 4473, u'uri': u'http://api.achaea.com/news/poetry.json', u'name': u'Poetry'}, {u'total': 449, u'uri': u'http://api.achaea.com/news/events.json', u'name': u'Events'}]

And lots more...