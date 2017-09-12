# Miss America's Faces
These scripts scrape, process, and average the images of the previous Miss America contest winners. The averaging approach is very naive, but it works decently.

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

If you want to change the number of averaged faces it produces (default is 4 different images), edit N_AVERAGES in faceMerger.py