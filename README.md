# My Website
author: Preston Pan \
description: My minimal, js-free website.

## Introduction
I decided to make a website because I always thought that web development was super frustrating.
Turns out, it still is, and I'm really bad at making websites. Let's just call it minimal.

Jokes aside, the website is actually designed to be as minimal as possible. With less than 70 lines of css,
the use of a self made static site generator instead of frontend javascript, and with other optimizations, 
each page can load within less than a second. No ads, trackers, javascript bloat,
or other nasties.

Due to the minimalistic nature of the website, fonts are locally stored and there are no google fonts to render.

## building
To generate and open the website, run the website.sh script with:
`./website.sh build`
A build folder in the same directory as that script will be generated. Simply open `index.html` in your browser. Note that
the fonts will not display until after you actually deploy the
website, due to me refering to the fonts via global path in my
css file, which is really an html file in templates by the name of
of `style.html`.

Link to the website is https://prestonpan.tech. 
Onion link is: http://4ugiqvhd7mrofdcubx5in4srqpmpsskwx4dpjps4waou5aksvoyk6vad.onion/.
