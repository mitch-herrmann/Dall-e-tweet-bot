def main(data, context):
  import os
  import requests
  import tweepy
  from datetime import datetime
  

  twitter_consumer_key = os.environ["twitter_consumer_key"]
  twitter_consumer_secret = os.environ["twitter_consumer_secret"]
  twitter_access_token = os.environ["twitter_access_token"]
  twitter_access_token_secret = os.environ["twitter_access_token_secret"]
  dalle_key = os.environ["dalle_key"]
  news_API_key = os.environ["news_API_key"]
  today_date = datetime.today().strftime('%Y-%m-%d')

  dalle_url = "https://api.openai.com/v1/images/generations"
  GPT_url = "https://api.openai.com/v1/completions"
  dalle_header = {
      "Authorization": f"Bearer {dalle_key}",
      "Content-Type": "application/json"}



  url = "https://newsapi.org/v2/everything"
  headers = {
      "X-Api-Key": news_API_key}
  params = {
      "q": "",
      "sources": "reuters",
      "from": today_date,
      "to": today_date
  }


  auth = tweepy.OAuth1UserHandler(
    twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret
  )
  api = tweepy.API(auth)
  
  def gpt(search_key):
      GPT_params = {
          "model": "text-davinci-003",
          "max_tokens": 75,
          "prompt": f"What are the best 3 terms to hashtag from this tweet (excluding anything with reuters): '{search_key}'",
          "temperature": 0.9,
      }
      GPT_response = requests.post(url=GPT_url, headers=dalle_header, json=GPT_params).json()
      return GPT_response['choices'][0]['text'].lstrip("\n")

  def dalle(search_key, article_url):
      dalle_params = {
          "prompt": search_key,
          "n": 1,
          "size": "1024x1024"
      }
      new_image = requests.post(url=dalle_url, headers=dalle_header, json=dalle_params).json()
      print("First dalle request ran")
      try:
          image_url = new_image["data"][0]["url"]
      except KeyError:
          return False
      else:
          hashtags = gpt(search_key)
          img_data = requests.get(image_url).content
          with open(f"/tmp/{search_key}.png", "wb") as handler:
              handler.write(img_data)
          print("Image saved")
          media = api.media_upload(filename=f"/tmp/{search_key}.png")
          print("Media uploaded")
          api.update_status(status=f"{search_key}\n{hashtags} #dalle #openai\n{article_url}", media_ids=[media.media_id])
          print("Tweet posted")
          return True


  def news_api():
      top_news = requests.get(url=url, params=params, headers=headers).json()
      print(top_news)
      articles = top_news["articles"]
      print(articles)
      tweet_posted = False
      for i in range(len(articles)):
          if "covid" in articles[i]["title"].lower():
              new_title = articles[i]["title"].replace("COVID", "Virus")
              articles[i]["title"] = new_title
          while tweet_posted == False:
            print(f"Trying dalle. Article title: {articles[i]['title']}")
            tweet_posted = dalle(search_key=articles[i]["title"], article_url=articles[i]["url"])
            print(tweet_posted)
            if tweet_posted == False:
                break
            else:
                return "OK"
  
  news_api()
