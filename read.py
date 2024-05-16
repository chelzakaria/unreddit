# this converts a zst file to csv
#
# it's important to note that the resulting file will likely be quite large
# and you probably won't be able to open it in excel or another csv reader
#
# arguments are inputfile, outputfile, fields
# call this like
# python to_csv.py wallstreetbets_submissions.zst wallstreetbets_submissions.csv author,selftext,title

import zstandard
import os
import json
import sys
import csv
from datetime import datetime
import logging.handlers


log = logging.getLogger("bot")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())


def read_and_decode(
    reader, chunk_size, max_window_size, previous_chunk=None, bytes_read=0
):
    chunk = reader.read(chunk_size)
    bytes_read += chunk_size
    if previous_chunk is not None:
        chunk = previous_chunk + chunk
    try:
        return chunk.decode()
    except UnicodeDecodeError:
        if bytes_read > max_window_size:
            raise UnicodeError(
                f"Unable to decode frame after reading {bytes_read:,} bytes"
            )
        return read_and_decode(reader, chunk_size, max_window_size, chunk, bytes_read)


def read_lines_zst(file_name):
    with open(file_name, "rb") as file_handle:
        buffer = ""
        reader = zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(
            file_handle
        )
        while True:
            chunk = read_and_decode(reader, 2**27, (2**29) * 2)
            if not chunk:
                break
            lines = (buffer + chunk).split("\n")

            for line in lines[:-1]:
                yield line, file_handle.tell()

            buffer = lines[-1]
        reader.close()


if __name__ == "__main__":
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    fields = sys.argv[3].split(",")
    # submissions
    # id,author,author_flair_text,title,selftext,link_flair_text,thumbnail,created_utc,permalink,score,hide_score,num_comments,media,media_embed,over_18

    # comments
    # id,author,author_flair_text,body,created_utc,score,score_hidden,permalink,parent_id,link_id,subreddit,subreddit_id

    file_size = os.stat(input_file_path).st_size
    file_lines = 0
    file_bytes_processed = 0
    line = None
    created = None
    bad_lines = 0
    output_file = open(output_file_path, "w", encoding="utf-8", newline="")
    writer = csv.writer(output_file)
    writer.writerow(fields)
    try:
        for line, file_bytes_processed in read_lines_zst(input_file_path):
            try:
                obj = json.loads(line)
                output_obj = []
                for field in fields:
                    if field not in obj:
                        output_obj.append("")
                        continue
                    if field == "created_utc":
                        output_obj.append(datetime.utcfromtimestamp(int(obj[field])))
                    else:
                        output_obj.append(
                            str(obj[field]).encode("utf-8", errors="replace").decode()
                        )
                writer.writerow(output_obj)

                created = datetime.utcfromtimestamp(int(obj["created_utc"]))
            except json.JSONDecodeError as err:
                bad_lines += 1
            file_lines += 1
            if file_lines % 100000 == 0:
                log.info(
                    f"{created.strftime('%Y-%m-%d %H:%M:%S')} : {file_lines:,} : {bad_lines:,} : {(file_bytes_processed / file_size) * 100:.0f}%"
                )
    except KeyError as err:
        log.info(f"Object has no key: {err}")
        log.info(line)
    except Exception as err:
        log.info(err)
        log.info(line)

    output_file.close()
    log.info(f"Complete : {file_lines:,} : {bad_lines:,}")
