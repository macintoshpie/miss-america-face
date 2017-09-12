import re
import os

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, URLopener

"""
This script scrapes the pictures of all of the previous Miss Americas from the
Miss America website. The pictures are saved to "pictures/original". Each
picture will be named the year of the cometition they won.
"""

ORIGINALS_PATH = 'pictures/original/'

BASE_URL = 'http://missamerica.org'
PICS_URL = BASE_URL + '/former-miss-americas/'

ImageOpener = URLopener()

def downloadImage(imgURL, imgName):
	ImageOpener.retrieve(imgURL, ORIGINALS_PATH + imgName + '.jpg')


# create directory for processed images if it doesn't exist
if not os.path.exists(ORIGINALS_PATH):
    os.makedirs(ORIGINALS_PATH)

# Make a request for the site and open with beautifulsoup
siteRequest = Request(PICS_URL, headers={'User-Agent': 'Mozilla/5.0'})
missASite = urlopen(siteRequest).read()
soup = BeautifulSoup(missASite, "lxml")

# info for each winner is in a table cell
winnerList = soup.find_all('td')
print("Found {} tds. There could be empty cells...".format(len(winnerList)))

# download the linked image for each winner
for idx, winner in enumerate(winnerList):
	# parse the contest year from the text
	try:
		winnerYear = re.search('\d{4}', winner.text).group(0)
	except AttributeError:
		# There could be blank cells used for padding
		continue

	# get the image url
	winnerImgURL = winner.find_all('img')[0]['src']
	# Make sure all urls are the full path
	try:
		re.search(BASE_URL, winnerImgURL).group(0)
	except AttributeError:
		winnerImgURL = BASE_URL + winnerImgURL

	# download the image, giving it the name of the contest year
	print("downloading: {}".format(winnerImgURL))
	downloadImage(winnerImgURL, winnerYear)