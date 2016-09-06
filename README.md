# [RapStock.io] (http://www.rapstock.io/tutorial/) - Fantasy Football Meets Hip Hop 
---
### Open Sourced Files
Made public a couple of the most important files from the private RapStock.io repo:
  * [views.py] (https://github.com/NipunSingh/RapStock.io/blob/master/views.py) - the controller in the Model-View-Controller architecture of the web app. Contains the business logic for users to discover new artists, to make investments in artists, to sell shares of artists, and to manage their portfolios.
  * [pricing_algorithm.py] (https://github.com/NipunSingh/RapStock.io/blob/master/pricing_algorithm.py) - the algorithm that would run hourly. It take the popularity metrics for each artist from Spotify and then comes up with a price for that artist's stock.
  * [models.py] (https://github.com/NipunSingh/RapStock.io/blob/master/models.py) - the data model. The actual file isn't very interesting so here is an ER diagram to explain the database design.

### Game Background

#### Video Summary
 An [awesome video] (http://www.youtube.com/watch?v=pNJl2YioTrc) which summarizes RapStock.io. It was produced by HackCville Media - a UVA club which chronicles the story of entrepreneurial people and projects. 

#### Full Background
As a life long music fan ([and former DJ!] (https://www.facebook.com/DJLilSingh/)), I have always been interested in discovering artists and songs before they were 'hot'. Nothing was better than that feeling of discovering an underground artist who blows up a year later. I wanted to make a game around that feeling - a game centered around predicting which rappers would become popular. And so with what little Python I knew I embarked on my first major individual coding project during my sophmore year of college winter break & spring semester (Dec'14 - Apr'15).  

I made the game mechanics similar to Fantasy Football or a virtual stock market game. Players would draft/invest in rappers who they think will become succesful. An [algorithm] (https://github.com/NipunSingh/RapStock.io/blob/master/pricing_algorithm.py) on my end would keep track of the popularity of all the artists. Players could see how well they were doing and compete for rewards and bragging rights. 

### Traction

At its peak RapStock.io had 2,000 Monthly Active Users with an average user session time of 6 minutes and 30 seconds. We entered the idea into the [Darden Business School's Effectual De-Risking Competition] (http://www.darden.virginia.edu/news/2015/darden-names-winner-from-3rd-annual-effectual-de-risking-competition/) and won 2nd place + $1500. We also got to pitch to Alexis Ohanian, YC Partner and Reddit Co-Founder, who was pretty impressed with our average user session time!

### Tech Stack
  * Python / Django
  * Hosted on Heroku
  * PostgreSQL
  * JQuery
  * Twitter Bootstrap
