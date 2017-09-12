import os
import math

from PIL import Image, ImageOps
import face_recognition
import numpy as np

"""
Once images are downloaded with imgScraper.py, run this script to format them.
Each image is adjusted and cropped so that the outer parts of the eyes are in 
the same location for every picture. Note that IMG_SIZE must be the same when 
running faceMerger.py. 
"""

IMG_SIZE = 300
EYE_HEIGHT = int(IMG_SIZE/3)
LEFT_EYE_NORMAL = (int(IMG_SIZE*.3), EYE_HEIGHT)
RIGHT_EYE_NORMAL = (int(IMG_SIZE*.7), EYE_HEIGHT)
NORMAL_X_DIST = RIGHT_EYE_NORMAL[0] - LEFT_EYE_NORMAL[0]

ORIGINALS_PATH = 'pictures/original/'
PROCESSED_PATH = 'pictures/processed/'

def ScaleRotateTranslate(image, angle, center = None, new_center = None, scale = None,expand=False):
	"""
	Given certain parameters, this function performs and Affine transformation
	of the image. This function was taken from user bytefish, provided in this
	stackoverflow post:
	https://stackoverflow.com/questions/7501009/affine-transform-in-pil-python
	"""
	if center is None:
		return image.rotate(angle)
	angle = -angle/180.0*math.pi
	nx,ny = x,y = center
	sx=sy=1.0
	if new_center:
		(nx,ny) = new_center
	if scale:
		(sx,sy) = scale
	cosine = math.cos(angle)
	sine = math.sin(angle)
	a = cosine/sx
	b = sine/sx
	c = x-nx*a-ny*b
	d = -sine/sy
	e = cosine/sy
	f = y-nx*d-ny*e
	return image.transform(image.size, Image.AFFINE, (a,b,c,d,e,f), resample=Image.BICUBIC)

def calculateTransformation(lefteye, righteye):
	"""
	Given the left and right eye positions, this function calculates the
	rotation and scaling needed to match the eyes to the normal positions
	"""
	# calculate the rotation needed
	if lefteye[1] > righteye[1]:
		# left eye is below right eye
		opposite = righteye[1] - lefteye[1]

	else:
		# left eye is above right eye
		opposite = righteye[1] - lefteye[1]

	hypotenuse = math.sqrt((lefteye[0] - righteye[0])**2 + (lefteye[1] - righteye[1])**2)

	rotateDegrees = math.degrees(math.asin(opposite/hypotenuse))

	thisDist = righteye[0] - lefteye[0]

	scale = NORMAL_X_DIST / thisDist

	return rotateDegrees, scale


# get file names
try:
	picNames = [x for x in os.listdir(ORIGINALS_PATH) if x.endswith(".jpg")]
except FileNotFoundError:
	raise Exception("The directory {} does not exist. Run imgScraper.py before continuing.".format(ORIGINALS_PATH))

if len(picNames) == 0:
	raise Exception("There are no pictures in {}. Run imgScraper.py before continuing.".format(ORIGINALS_PATH))

# create directory for processed images if it doesn't exist
if not os.path.exists(PROCESSED_PATH):
    os.makedirs(PROCESSED_PATH)

# an array to hold names of images where faces could not be found
noFacesFound = []

# Process each picture
for idx, imgName in enumerate(picNames):
	print("processing {}...".format(imgName))
	# open the image and insert it into a larger array in order to have a bigger picture
	origImg = np.array(Image.open(ORIGINALS_PATH + imgName).convert("RGB"), dtype=np.float)
	largerImg = np.zeros((IMG_SIZE, IMG_SIZE, 3), np.float)
	largerImg[0:origImg.shape[0], 0:origImg.shape[1]] = origImg
	img = Image.fromarray(np.array(np.round(largerImg), dtype=np.uint8))

	# get face landmarks 
	landmarksImg = face_recognition.load_image_file(ORIGINALS_PATH + imgName)
	try:
		landmarks = face_recognition.face_landmarks(landmarksImg)[0]
	except IndexError:
		# if no landmarks were found, skip this picture
		noFacesFound.append(imgName)
		continue

	# get the outer points of the left and right eyes
	outerLeftEye = landmarks['left_eye'][0]
	outerRightEye = landmarks['right_eye'][3]

	# transform image to align eyes
	degs, scaling = calculateTransformation(outerLeftEye, outerRightEye)
	print("rotating {} degrees, scaling by {}".format(degs, scaling))
	img = ScaleRotateTranslate(img, angle=degs, center=outerLeftEye, new_center=LEFT_EYE_NORMAL, scale=(scaling, scaling))

	# save the image
	img.save(PROCESSED_PATH + imgName)

if noFacesFound:
	print("Unable to find faces for the files below:")
	for img in noFacesFound:
		print(img)

else:
	print("Found faces for all images")