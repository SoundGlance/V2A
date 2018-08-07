# Web Segmentation

Implementation of ["Purely vision-based segmentation of web pages 
for assistive technology"](https://www.sciencedirect.com/science/article/pii/S1077314216000527) 
with several simplications and revisions.

## Dependency

Python libraries

* numpy
* scipy
* pillow

## Example

```bash
cd segmentation
python3 segmentation.py naver_webtoon.png [max_depth]
```

* This code loads image named `naver_webtoon.png` 
* from the directory `/segmentation/sample_data`
* and recursively segment the image until it reach the max_depth (6 if unspecified)
* the results are saved in the same directory above

![a sample result of segmentation](https://media.giphy.com/media/OkhB2rUZbDqivUhOFQ/giphy.gif)
