# CommentHarvester

 CommentHarvester is a powerful tool designed for efficiently scraping YouTube comments from videos. It extracts user comments, metadata (such as likes, timestamps, and replies), and performs sentiment analysis or keyword filtering. Ideal for content creators, marketers, and researchers looking to analyze audience engagement and trends.

# setup

1. Create a Python virtual environment and install the required modules:

```sh
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

2. Set up the environment variable for the YouTube API key:

```sh
export YOUTUBE_API_KEY={YOUR API KEY HERE}
```

# run

```
python3 main.py
```

and input the video id from the youtube link
