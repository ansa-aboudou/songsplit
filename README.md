# SongSplit
<p align="center"><img src="https://github.com/ansa-aboudou/songsplit/blob/master/media/logo.png" width="128px"><p>
SongSplit is an App that allows you to seperate the vocals from the beat of a song thanks to a pretrained models developed by Deezer (Spleeter), this model is written in Python and uses Tensorflow.<br><br>
Drag and drop your audio file then downloads you outputs.
Live demo availaible here : http://songsplit.herokuapp.com/<br>
Please find in a demo audio file.<br>
Slow Motion Dream by Steven M Bryant (c) copyright 2011 Licensed under a Creative Commons Attribution (3.0) license. http://dig.ccmixter.org/files/stevieb357/34740 Ft: CSoul,Alex Beroza & Robert Siekawitch<br>
Login and purchase (Fake functionnality with Stripe : https://stripe.com/docs/testing) before using.<br>
<br>
<p align="center"><img src="https://raw.githubusercontent.com/ansa-aboudou/songsplit/master/media/landing.jpg"><p>
<hr>
<p align="center"><img src="https://raw.githubusercontent.com/ansa-aboudou/songsplit/master/media/home.jpg"><p>
<hr>
<p align="center"><img src="https://raw.githubusercontent.com/ansa-aboudou/songsplit/master/media/landing_mobile.jpg"><p>
<hr>
<p align="center"><img src="https://raw.githubusercontent.com/ansa-aboudou/songsplit/master/media/home_mobile.jpg"><p>

## Setup
```
git clone https://github.com/ansa-aboudou/songsplit
cd songsplit
pip install -r requirements.txt
python app.py
```

## Disclaimer
You may meet some memory issue particularly when using the app on heroku, so please try to upload light files.
We could improve this project by converting the model into tensorflowjs.

## Credits
<br>
These repositories helped me build this project, thank you guys :) :<br>
- https://github.com/deezer/spleeter
- https://github.com/anfederico/Flaskex