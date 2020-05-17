#!/usr/bin/env python3

import argparse, csv, requests
import numpy as np
from urllib.parse import urljoin

parser = argparse.ArgumentParser(description="Process some integers.")
parser.add_argument("config_url", help="config url")

def fetch_config(url):
    config = requests.get(url).json()
    config["input_file_data"] = requests.get(urljoin(url, config["input_file_name"])).json()

    return config

def process(data, output_file_name):
    frames = data["frames"]

    boxes = dict()

    for key in frames:
        for item in frames[key]:
            if "box" in item:
                try:
                    boxes[item["idx"]]
                except KeyError:
                    boxes[item["idx"]] = []
                boxes[item["idx"]].append(item["box"])

    with open(output_file_name, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "avg_area", "min_area", "max_area"])
        for id in boxes:
            values = np.array([(coords[2]-coords[0])*(coords[3]-coords[1]) for coords in boxes[id]])
            writer.writerow([id, np.average(values), np.min(values), np.max(values)])

if __name__ == "__main__":
    args = parser.parse_args()
    config = fetch_config(args.config_url)
    process(config["input_file_data"], config["output_file_name"])
