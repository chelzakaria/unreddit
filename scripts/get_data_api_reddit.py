from datetime import datetime, date, timedelta
from typing import Optional
from tqdm import tqdm
import logging as log
import pandas as pd
import requests
import calendar

log.basicConfig(
    filename="reddit_api_logs.log",
    encoding="utf-8",
    level=log.INFO,
    format="%(asctime)s--%(message)s",
)


def get_data_api_reddit(
    subreddit: str,
    start_date: str,
    end_date: Optional[str] = datetime.now().strftime("%Y-%m-%d"),
    output_path: str = "output.csv",
    option: str = "submissions",
):
    """
    Get data from Reddit API

    Args:
        subreddit: str: subreddit name
        start_date: str: start date in format "YYYY-MM-DD"
        end_date: str: end date in format "YYYY-MM-DD" (default: today)
        output_path: str: output file path (default: output.csv)
        option: str: data type to get (submissions or comments) (default: submissions)

    Returns:
        None
    """

    if option == "submissions":
        base_url = (
            f"https://api.pullpush.io/reddit/submission/search?subreddit={subreddit}"
        )
        fields = [
            "id",
            "author",
            "author_flair_text",
            "title",
            "selftext",
            "link_flair_text",
            "thumbnail",
            "created_utc",
            "permalink",
            "score",
            "hide_score",
            "num_comments",
            "media",
            "media_embed",
            "over_18",
        ]
    elif option == "comments":
        fields = [
            "id",
            "author",
            "author_flair_text",
            "body",
            "created_utc",
            "score",
            "score_hidden",
            "permalink",
            "parent_id",
            "link_id",
            "subreddit",
            "subreddit_id",
        ]
        base_url = (
            f"https://api.pullpush.io/reddit/comment/search?subreddit={subreddit}"
        )

    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()

    dataframe = pd.DataFrame(columns=fields)

    for i in tqdm(range((end_date - start_date).days)):
        log.info(
            f"Getting {option} data from {start_date + timedelta(days=i)} to {start_date + timedelta(days=i + 1)}"
        )
        url = f"{base_url}&since={calendar.timegm((start_date + timedelta(days=i)).timetuple())}&until={calendar.timegm((start_date + timedelta(days=i + 1)).timetuple())}"
        try:
            data = requests.get(url, timeout=20).json()["data"]
        except:
            log.error(
                f"Error in getting {option} data from {start_date - timedelta(days=i)} to {start_date - timedelta(days=i - 1)}"
            )
            continue
        log.info(f"Founds {len(data)} {option} data")
        row = []
        for item in data:
            for field in fields:
                if field == "created_utc":
                    row.append(datetime.utcfromtimestamp(int(item[field])))
                else:
                    row.append(str(item[field]))
            dataframe.loc[len(dataframe)] = row
            row = []

    dataframe.to_csv(output_path, encoding="utf-8")


start_date = "2009-01-01"
end_date = "2024-05-24"

# get subreddit submissions
get_data_api_reddit(
    "morocco",
    start_date,
    end_date,
    output_path=f"data/morocco/submissions_{start_date}_{end_date}.csv",
    option="submissions",
)

# get subreddit comments
get_data_api_reddit(
    "morocco",
    start_date,
    end_date,
    output_path=f"data/morocco/comments_{start_date}_{end_date}.csv",
    option="comments",
)
