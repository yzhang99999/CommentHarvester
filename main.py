from googleapiclient.discovery import build
import csv
import os
import click

def get_comment(video_id: str):
  # Replace with your API key and video ID
  api_key = os.getenv("YOUTUBE_API_KEY")
  # Build the YouTube service
  youtube = build("youtube", "v3", developerKey=api_key)

  # List to store comments data
  comments = []
  page_count = 0

  # Fetch comments with pagination
  next_page_token = None
  while True:
      response = youtube.commentThreads().list(
          part="snippet,replies",
          videoId=video_id,
          maxResults=100,
          pageToken=next_page_token if next_page_token else None
      ).execute()

      page_count += 1
      print(f"Processing page {page_count}, fetched {len(response['items'])} items")

      for item in response["items"]:
          # Top-level comment
          snippet = item["snippet"]["topLevelComment"]["snippet"]
          comments.append({
              "text": snippet["textDisplay"],
              "author": snippet["authorDisplayName"],
              "date": snippet["publishedAt"],
              "likes": snippet["likeCount"],
              "type": "top-level"
          })

          # Replies (if any)
          if "replies" in item:
              for reply in item["replies"]["comments"]:
                  reply_snippet = reply["snippet"]
                  comments.append({
                      "text": reply_snippet["textDisplay"],
                      "author": reply_snippet["authorDisplayName"],
                      "date": reply_snippet["publishedAt"],
                      "likes": reply_snippet["likeCount"],
                      "type": "reply"
                  })

      # Check for next page
      next_page_token = response.get("nextPageToken")
      if not next_page_token:
          break
  return comments

@click.command()
@click.option('--video-id', '-v', prompt='Enter the YouTube video ID', help='The ID of the YouTube video.')
@click.option('--output-path', '-o', default='.', help='The directory where the CSV file will be saved.')
def main(video_id, output_path):
    csv_file = os.path.join(output_path, f"{video_id}_comments.csv")
    comments = get_comment(video_id)

    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["text", "author", "date", "likes", "type"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for comment in comments:
            writer.writerow(comment)

    print(f"Total extracted: {len(comments)} comments/replies, saved to {csv_file}")

if __name__ == "__main__":
    main()