# Dall-E Tweet Bot
A routine that finds top news headlines on Reuters and posts a tweet about the article, with an image output by OpenAI's Dall-E and hashtags determined by ChatGPT. This was designed to run as a Cloud Function on Google Cloud Platform and was run hourly via a Cron Job to post tweets under the Twitter account The_Dall_E_News (https://x.com/the_Dall_E_News), which was active until I ran out of OpenAI credits. 

### Software Requirements
- This code was written using Python 3.10
- a Twitter account and Tweepy
- An OpenAI account