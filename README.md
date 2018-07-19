# Web Segmentation

Implementation of ["Purely vision-based segmentation of web pages 
for assistive technology"](https://www.sciencedirect.com/science/article/pii/S1077314216000527) 
with several simplications and revisions. **Still in development!!**

## Dependency

Python libraries

* numpy
* scipy
* pillow

## examples

```bash
cd segmentation
python3 segmentation.py naver_webtoon.png
```

This code loads image named `naver_webtoon.png` from the directory `/segmentation/sample_data` and save the results at the same folder.

![a sample result of segmentation](https://media.giphy.com/media/OkhB2rUZbDqivUhOFQ/giphy.gif)
