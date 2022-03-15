- ~~resize and crop thumbnail images locally with imagemagick~~
- popover text for teasers?
https://codepen.io/chocochip/pen/zYxMgRG

- Pagination
https://betterprogramming.pub/simple-flask-pagination-example-4190b12c2e2e
https://www.adamsmith.haus/python/answers/how-to-take-a-subset-of-a-dictionary-in-python

- Add more content
  
- ~~Group by tag (e.g. "B-Lab", "One-pages", "I Am a Pineapple", etc.)~~


# NOTES

Making thumbnails:
```
mogrify -resize 480x480^ -gravity center -extent 440x440 *
```

Making fulls:
```
mogrify -resize 1920x\> * 
```