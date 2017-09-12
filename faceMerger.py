import os

from PIL import Image
import numpy as np

"""
After processing images with facesFormatter.py, run this script to merge the
faces. Depending on the value of N_AVERAGES, the script will divide the 
pictures into N_AVERAGES evenly sized groups for separate average images,
ordered by year. The averaged pictures will be saved in /pictures/
"""

IMG_SIZE = 300
RGB_DIM = 3

N_AVERAGES = 4
AVG_PIC_IDX = [i/N_AVERAGES for i in range(1, N_AVERAGES+1)]

PROCESSED_PATH = 'pictures/processed/'

def getImgIndex(picPosition):
	"""
	Given the index of the picture name, this function returns the index of
	its averaged image in the list of averaged images
	"""
	arrayIdx = 0

	while AVG_PIC_IDX[arrayIdx] < picPosition:
		arrayIdx += 1

	return arrayIdx


# an array to hold our averaged picture array(s)
avgPics = [np.zeros((IMG_SIZE, IMG_SIZE, 3), np.float) for i in range(N_AVERAGES)]
# for i in range(N_AVERAGES):
# 	avgPics.append(np.zeros((IMG_SIZE, IMG_SIZE, 3), np.float))

# get file names
try:
	picNames = [x for x in os.listdir(PROCESSED_PATH) if x.endswith(".jpg")]
except FileNotFoundError:
	raise Exception("The directory {} does not exist. Run facesFormatter.py before continuing.".format(PROCESSED_PATH))

if len(picNames) == 0:
	raise Exception("There are no pictures in {}. Run facesFormatter.py before continuing.".format(PROCESSED_PATH))

# multiply nPicFiles by 2 because we are also averaging each image after flipping it vertically
nPicFiles = len(picNames)
nPicsAveraged = nPicFiles * 2


# Average the images
for idx, imgName in enumerate(picNames):
	# calculate the picture's position
	picPos = idx / (nPicFiles)
	avgPicIdx = getImgIndex(picPos)
	print("processing {} for set {}...".format(imgName, avgPicIdx))

	

	# Open image and make sure it's RGB
	img = Image.open(PROCESSED_PATH + imgName).convert("RGB")

	# turn image into an array
	arrayImg = np.array(img, dtype=np.float)

	# add it to its average picture
	avgPics[avgPicIdx] = avgPics[avgPicIdx] + (arrayImg/nPicsAveraged)

	# flip the image and add it to its average
	arrayImg = np.fliplr(arrayImg)
	avgPics[avgPicIdx] = avgPics[avgPicIdx] + (arrayImg/nPicsAveraged)

# Save each averaged image
for idx, pic in enumerate(avgPics):
	# get the starting year and ending year for each averaged picture
	try:
		startName = picNames[int(AVG_PIC_IDX[idx-1]*(nPicFiles) + 1)]
	except IndexError:
		startName = picNames[0]
	try: 
		endName = picNames[int(AVG_PIC_IDX[idx]*(nPicFiles))]
	except IndexError:
		endName = picNames[-1]

	startName = startName[0:4]
	endName = endName[0:4]

	# save the picture
	pic = np.array(np.round(pic), dtype=np.uint8)
	img = Image.fromarray(pic)
	filename = 'AverageFace_' + startName + '-' + endName + '.jpg'
	img.save('pictures/' + filename)