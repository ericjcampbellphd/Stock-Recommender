# Stock-Recommender

This repo demonstrates a machine-learning random-forest model to predict whether a brick-and-mortar stock 
should be sold or bought prior to its quarterly earnings-per-share (EPS) release. Stock prices are known to jump or drop
noticably after an EPS release depending on the sentiment of the report.

The deployed app can be accessed <a href="http://eric-j-campbell-capstone.herokuapp.com/">here</a>. Please allow the app up to 30 seconds to load.

The principal features of the model are accessed through a Facebook dataset, which tracks the Likes, Check-ins, and Talking-about-counts for 
thousands of companies over a 2 year period. Financial data is also scraped from Yahoo Finance using Beautiful Soup and pulled from Intrinio API
using Requests.

To link company name to stock ticker, the Fuzzy-Wuzzy library is used along with the Intrinio API to determine if a company is publicly-traded,
allowing for its stock price data to be accessed.

The model is compared to a naive approach in which a Dow-Jones Index fund is used for comparison.

The model is not perfect, as is the stochastic nature of the stock market. On occasion, it predicts investments which generate 7% bumps in portfolio
yield in a single day. Conversely, it also predicts investments which generate portfolio losses. In these instances, it is important to have a diversified portfolio.

To conclude and reflect, check-ins can serve as a valuble metric to predicting how well a brick-and-mortar store is performing, though it is not the only factor.
For instance: 
<ul>
<li>Many companies are conglomorates, so the performance of one sub-company may not correlate to the overall stock performance.</li>
<li>Recessions, booms, acquisitions, mergers, innovations, and scandals can all affect the sentiment of investors, and therefore the trends in share prices themselves.</li>
<li>Check-ins may be misleading. For instance, Planet Fitness may have many new memberships, but people lose their new years convictions and stop checking in at the gym. 
On the flip side, people may do sit-ins at Starbucks in protest while checking in but not buying anything.</li>
</ul>

This model has the potential to better predict stock price jumps or drops after a quarterly EPS release. More financial data could be used as features in addition
to sentiments from financial company ratings and articles about the outlook for each company.
