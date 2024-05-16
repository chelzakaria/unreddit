import requests
from datetime import datetime, date
import pandas as pd
from tqdm import tqdm
import logging as log

log.basicConfig(
    filename="reddit_api_logs.log",
    encoding="utf-8",
    level=log.INFO,
    format="%(asctime)s--%(message)s",
)


def get_comments_api_reddit(subreddit: str, submission_id: str):
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

    base_url = f"https://api.pullpush.io/reddit/search/comment/?link_id={submission_id}"

    df = pd.DataFrame(columns=fields)
    row = []
    try:
        data = requests.get(base_url, timeout=60).json()["data"]
    except:
        log.error(f"Error in getting comments for {submission_id}")
        return df
    for item in data:
        for field in fields:
            if field == "created_utc":
                row.append(datetime.utcfromtimestamp(int(item[field])))
            else:
                row.append(str(item[field]))
        df.loc[len(df)] = row
        row = []

    return df


def get_data_api_reddit(
    subreddit: str,
    from_date: str,
    to_date: str,
    epoch: str,
    submissions_output_path: str = "subs_output.csv",
    comments_output_path: str = "comments_output.csv",
):
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
    base_url = f"https://api.pullpush.io/reddit/search/submission/?subreddit={subreddit}&sort=asc"

    if not to_date:
        to_date = datetime.now().strftime("%Y-%m-%d")

    to_date = datetime.strptime(to_date, "%Y-%m-%d")
    from_date = datetime.strptime(from_date, "%Y-%m-%d")
    start_day = (datetime.now() - from_date).days
    end_day = (datetime.now() - to_date).days
    # start_hour = start_day * 24 + datetime.now().hour

    # diff = to_date - from_date

    # days, seconds = diff.days, diff.seconds
    # hours = days * 24 + seconds // 3600

    # with open(output_path, "w") as f:
    #     f.write(",".join(fields) + "\n")

    output_dict = {}
    subs_dataframe = pd.DataFrame(columns=fields)
    comments_dataframe = pd.DataFrame()
    if epoch == "days":
        for i in tqdm(range(start_day, end_day, -1)):
            log.info(f"Getting data for {i} days ago")
            url = f"{base_url}&after={i}d&before={(i-1)}d"
            try:
                data = requests.get(url, timeout=20).json()["data"]
            except:
                log.error(f"Error in getting data for {i} days ago")
                continue
            row = []
            for item in data:
                for field in fields:
                    if field == "created_utc":
                        row.append(datetime.utcfromtimestamp(int(item[field])))
                    else:
                        row.append(str(item[field]))
                subs_dataframe.loc[len(subs_dataframe)] = row
                row = []
                comments_dataframe = pd.concat(
                    [
                        comments_dataframe,
                        get_comments_api_reddit(subreddit, item["id"]),
                    ],
                    ignore_index=True,
                )

    subs_dataframe.to_csv(submissions_output_path, encoding="utf-8")
    comments_dataframe.to_csv(comments_output_path, encoding="utf-8")


get_data_api_reddit(
    "morocco",
    "2022-12-31",
    "2024-01-25",
    "days",
    submissions_output_path="morocco/output_2023.csv",
    comments_output_path="morocco/comments_2023.csv",
)
