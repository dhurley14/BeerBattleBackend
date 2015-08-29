from flask import Flask
from bs4 import BeautifulSoup
import requests

class Beer(object):
    def __init__(self, bname):
        self.name = bname

    def getName(self):
        return self.name

    def getAdvRating(self):
        self.name, page_link = self.find_beer_rating_page(self.name)
        rating = self.get_rating_from_page(page_link)
        return rating

    def getRBRating(self):
        print 'getRBRating: name: {0}'.format(self.name)
        results = self.rows_from_search(self.name)
        highest_number_of_ratings = 0
        the_rating = 0
        for row in results:
            print(type(row))
            num_ratings = 0
            try:
                num_ratings = int(row.find_all('td')[4].string)
            except:
                print "found string in int"
            rating = 0
            try:
                rating = int(row.find_all('td')[3].string)
            except:
                print "found string in int"
            if(num_ratings >= highest_number_of_ratings):
                highest_number_of_ratings = num_ratings
                print 'new highest_number_of_ratings: {0}'.format(num_ratings)
                the_rating = rating
                print 'new rating --> {0}'.format(the_rating)
        return the_rating

    def rows_from_search(self, bname):
        r = requests.post("http://www.ratebeer.com/findbeer.asp", {"BeerName":bname})
        soup = BeautifulSoup(r.text, 'html.parser')
        tables = soup.find_all('table')
        #rows = []
        try:
            rows = tables[0].find_all('tr')
            print type(rows[0])
            if type(rows[0]) is str:
                return 'No RateBeer Results'
            #print "length of rows from search:{0}".format(len(rows))
            return rows
        except:
            print "exception!!"
        #print "length of rows from search:{0}".format(len(rows))
        return 'No RateBeer Results'


    def find_beer_rating_page(self, name):
        # search beer advocate for
        print 'findBeerRatingPage({0})'.format(name)
        r = requests.get('http://www.beeradvocate.com/search/?q={0}'.format(name))
        soup = BeautifulSoup(r.text, 'html.parser')
        # print soup.prettify()
        print len(soup.find_all('a'))
        for link in soup.find_all('a'):
            # print link.get('href')
            the_link = link.get('href')
            the_beer = link.string
            print 'outer_link: {0}'.format(the_link)
            if the_link is not None:
                if('/beer/profile' in the_link):
                    print 'the_link: {0}'.format(the_link)
                    return the_beer, the_link
            # print 'Not Found :/'
        return 'Not Found'


    def get_rating_from_page(self, pageLink):
        # parse rating page
        r = requests.get('http://www.beeradvocate.com{0}'.format(pageLink))
        soup = BeautifulSoup(r.text, 'html.parser')
        for span_tag in soup.find_all('span'):
            the_class = span_tag.get('class')
            if the_class is not None:
                if 'BAscore_big' in the_class[0] and 'ba-score' in the_class[1]:
                    print 'found the rating: {0}'.format(span_tag.string)
                    return span_tag.string
        return 'Couldn\'t find the rating, sorry :/'
