# Miss America's Faces
These scripts scrape, process, and average the images of the previous Miss America contest winners. First, the images are downloaded from the Miss America site. Then the images are searched for facial landmarks using the face_recognition package. The outer points of the left and right eye are extracted to determine the rotation, scaling, and translation parameters. This is used to move the eyes to the same position for every picture. Stopping there for formatting is a bit naive, and the average picture suffer a bit due to the lack of warping, but it's all I feel like implementing currently. The faces are then averaged together. By default, the script bins the pictures into 4 groups, organized by date of cometition, and produces an average image for each group (e.g. an average picture for 1921-1949, 1951-1973, 1974-1995, and 1996-2017). To change the number of averaged faces it produces, edit N_AVERAGES in faceMerger.py.

### Packages required:
- beautiful soup
- urllib
- Python Imaging Library (PIL)
- numpy
- face_recognition

### How to use it:
1. Clone the repository
2. Run imgScraper.py
3. Run faceFormatter.py
4. Run faceMerger.py  
DONE

