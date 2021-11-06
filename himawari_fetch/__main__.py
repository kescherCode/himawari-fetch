#!/usr/bin/env python3

import argparse
import io
import itertools as it
import multiprocessing
import multiprocessing as mp
import multiprocessing.dummy as mp_dummy
import os
import os.path as path
import sys
import threading
import time
import requests
from datetime import timedelta, datetime
from glob import iglob

from PIL import Image

counter = multiprocessing.Value("i", 0)
HEIGHT = 550
WIDTH = 550


def download_chunk(args):
    global counter

    x, y, latest, level = args
    url_format = "https://himawari8-dl.nict.go.jp/himawari8/img/D531106/{}d/{}/{}_{}_{}.png"
    url = url_format.format(level, WIDTH, datetime.strftime(latest, "%Y/%m/%d/%H%M%S"), x, y)

    tile_data = download(url).content

    # If the tile data is 2867 bytes, it is a blank "No Image" tile.
    if tile_data.__sizeof__() == 2867:
        sys.exit('No image available for {}.'.format(datetime.strftime(latest, "%Y/%m/%d %H:%M:%S")))

    with counter.get_lock():
        counter.value += 1
        percent = (counter.value * 100) / (level * level)
        if percent % 25 == 0:
            print("Downloading tiles: {:.0f}% completed.".format(percent))
    return x, y, tile_data


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--deadline", type=int, dest="deadline", default=60,
                        help="deadline in seconds for this script to finish, set 0 to cancel")
    parser.add_argument("--output-dir", type=str, dest="output_dir",
                        help="directory to save images and metadata",
                        default="/tmp/himawari-data")
    parser.add_argument("--override-date", type=str, dest="override_date",
                        help="UTC timestamp in format '%%Y-%%m-%%d %%H:%%M:%%S'")
    args = parser.parse_args()
    if not args.deadline >= 0:
        sys.exit("Deadline has to be greater than (or equal to if you want to disable) zero!\n")

    return args


def download(url):
    exception = None

    for i in range(1, 4):  # retry max 3 times
        try:
            with requests.get(url) as response:
                return response
        except Exception as e:
            exception = e
            print("[{}/3] Retrying to download '{}'...".format(i, url))
            time.sleep(3)
            pass

    if exception:
        raise exception
    else:
        sys.exit("Could not download '{}'!\n".format(url))


def thread_main(args):
    global counter
    counter = mp.Value("i", 0)
    level = 20

    os.makedirs(path.dirname(args.output_dir), exist_ok=True)

    print("Checking...")
    latest_json = download("https://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json")
    latest = datetime.strptime(latest_json.json()["date"], "%Y-%m-%d %H:%M:%S")

    print("Latest version: {} UTC.".format(datetime.strftime(latest, "%Y/%m/%d %H:%M:%S")))
    date = latest
    if args.override_date is not None:
        if latest - date > timedelta(days=1, minutes=30):
            sys.exit("Overridden date is too far back in the past. Aborting.")
        if date > latest:
            sys.exit("Overridden date is newer than the latest available data. Aborting.")
        date = datetime.strptime(args.override_date, "%Y-%m-%d %H:%M:%S")
        print("Overridden version: {} UTC.".format(datetime.strftime(date, "%Y/%m/%d %H:%M:%S")))

    output_file = path.join(args.output_dir, datetime.strftime(date, "%Y%m%dT%H%M%S.png"))
    if os.path.isfile(output_file):
        print("Image already exists. Aborting.")
        sys.exit()

    png = Image.new("RGB", (WIDTH * level, HEIGHT * level))

    p = mp_dummy.Pool(level * level)
    print("Downloading tiles...")
    res = p.map(download_chunk, it.product(range(level), range(level), (date,), (level,)))

    for (x, y, tile_data) in res:
        tile = Image.open(io.BytesIO(tile_data))
        png.paste(tile, (WIDTH * x, HEIGHT * y, WIDTH * (x + 1), HEIGHT * (y + 1)))

    if (latest - date) == timedelta(0):
        threshold = latest - timedelta(days=1, minutes=30)
        for file in iglob(path.join(args.output_dir, "*.png")):
            _, filename = os.path.split(file)
            file_date = datetime.strptime(filename, "%Y%m%dT%H%M%S.png")
            if file_date < threshold:
                print("Deleting %s due to age" % (file,))
                os.remove(file)

    print("Saving to '%s'..." % (output_file,))
    os.makedirs(path.dirname(output_file), exist_ok=True)
    png.save(output_file, "PNG")
    if (latest - date) == timedelta(0):
        print("Saving latest timestamp...")
        timestamp_file = open(path.join(args.output_dir, "latest"), "w")
        timestamp_file.write(datetime.strftime(latest, "%Y%m%dT%H%M%S.png"))
        timestamp_file.close()


def main():
    args = parse_args()

    main_thread = threading.Thread(target=thread_main, args=(args,), name="himawari_fetch-main-thread", daemon=True)
    main_thread.start()
    main_thread.join(args.deadline if args.deadline else None)

    if args.deadline and main_thread.is_alive():
        sys.exit("Timeout!\n")

    print()
    sys.exit(0)


if __name__ == "__main__":
    main()
