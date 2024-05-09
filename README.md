# prophet-challenge
Module 8 Challenge ##Tools used: Co-pilot; XbertAssistant; ChatGpt

Here's a summary of actions taken to analyze MercadoLibre's search traffic and its potential correlations to financial events and stock price patterns, using Google Colab and the Prophet model for the time series forecasting:

Data Review and Visualization: 
Step 1: Search for Unusual Patterns, The Google search data was imported for review, particularly for May 2020 when MercadoLibre released its quarterly financial results. The analysis included visualizing search trends.  We calculated the total search traffic for May 2020 and compared it to the monthly median across all other months. 

Step 2: Mining the Search Traffic Data for Seasonality
Hourly Trends: The data was grouped and plotted to observe the average traffic by hour of the day, revealing specific times when search traffic peaked.
Daily and Weekly Trends: Further grouping provided insights into which days of the week experienced the most search traffic and how search patterns varied weekly throughout the year, especially during the winter holiday period from weeks 40 to 52.

Step 3: Relating Search Traffic to Stock Price Patterns
Data was Merged and Visualized: Search trend data and stock price data were merged into a single DataFrame and analyzed. 
New columns were added for lagged search trends, stock volatility and hourly stock returns.

Correlation Analysis: The relationship between lagged search traffic, stock volatility, and stock price returns, were analyzed to determine if there are any strong predictable relationships.

Step 4: Creating a Time Series Model with Prophet
Model Setup and Forecasting: The search data was formatted for the Prophet model, which was then used to forecast future search traffic trends.  
Forecast: The near-term forecast provides a favorable trend in MercadoLibre’s popularity. The model's output helps identify the most popular times of the day, busiest days of the week, and the lowest points in search traffic throughout the calendar year.

Conclusion
The project successfully utilized advanced data analytics and time series modeling to provide MercadoLibre with actionable insights on optimizing marketing strategies based on user search patterns. It also explored the interplay between external financial events and search behavior, offering guidance in strategic decision-making and financial forecasting. This comprehensive approach not only highlighted critical seasonal trends but also identified potential opportunities for enhancing customer engagement based on predictable search traffic patterns.