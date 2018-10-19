# import libraries
print("importing libraries...")
import pandas as pd
import glob
print("\nimporting libraries complete")

# Specify columns and dtypes
print("\n\nreading data...")
data = {
	"external_author_id":object,
    "author":object,
    "content":object,
    "region":object,
    "language":object,
    "publish_date":object,
    "harvested_date":object,
    "following":int,
    "followers":int,
    "updates":int,
    "post_type":object,
    "account_type":object,
    "retweet":bool,
    "account_category":object,
    "new_june_2018":bool,
    "alt_external_id":object,
    "tweet_id":object,
    "article_url":object,
    "tco1_step1":object,
    "tco2_step1":object,
    "tco3_step1":object
}

date_cols = ["publish_date", "harvested_date"]

# import files
files = glob.glob("*.csv")
#df = pd.concat([pd.read_csv(f, names = data.keys(), dtype = data, parse_dates = True) for f in files])
df = pd.concat([pd.read_csv(f, dtype = data, parse_dates = date_cols) for f in files])
print("\nreading data complete")

# explore
#df[['language', 'tweet_id']].groupby('language').count().sort_values('tweet_id', ascending = False)

# filter for english
english = df.loc[df['language'] == 'English']

# import sentiment analyzer
print("\n\nanalyzing sentiment...")
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

# apply sentiment analyzer to english df
#####res = [sid.polarity_scores(x) for x in df['content']]
sentiment = english['content'].astype(str).apply(lambda x : sid.polarity_scores(x))
english = pd.concat([english,sentiment.apply(pd.Series)],1)
df_merge = df.merge(english[["tweet_id", "neg", "neu", "pos", "compound"]], how = "left", on = "tweet_id")
print("\nanalyzing sentiment complete")

# write csv
print("\n\nwriting to csv...")
df_merge.to_csv("russian-troll-tweets.csv", index=False)
print("\nwriting to csv complete")