#!/bin/python3
import argparse
import os
import re
import csv
import json
from PIL import Image
from PIL.TiffImagePlugin import ImageFileDirectory_v2
import numpy as np

def header_file_to_dict(lines):
    o_dict = {}
    for line in lines:
        m = re.search("^([^:]+):\\s?", line)
        key = m.group(1)
        value = line[len(m.group(0)):]
        o_dict[key] = value.rstrip()
    return o_dict

def extract_ifcb_images(target, no_metadata = False):
    header_lines = ""
    with open(target + ".hdr") as f:
        header_lines = f.readlines()
    metadata = header_file_to_dict(header_lines)

    adc_format_map = list(csv.reader([metadata["ADCFileFormat"]], skipinitialspace=True))[0]
    image_map = []
    with open(target + ".adc") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=adc_format_map, skipinitialspace=True)
        with open(target + ".roi", "rb") as imagefile:
            for row in reader:
                #print(row)
                imagefile.seek(int(row["start_byte"]))
                height = int(row["ROIheight"])
                width = int(row["ROIwidth"])
                imdata = imagefile.read(height * width)
                imdata_reform = np.zeros([width, height], dtype=np.uint8)
                if (height * width > 0):
                    for y in range(0,height):
                        for x in range(0,width):
                            imdata_reform[x][y] = imdata[(y * width) + x]
                    image = Image.fromarray(imdata_reform, "L")
                    image_package = {"metadata": row, "image": image}
                    image_map.append(image_package)
                    im_metadata = {}
                    for col_key in row:
                        sanitised_col_key = re.sub(r"[^A-Za-z0-9_-]", "", col_key)
                        #print(sanitised_col_key)
                        #print(row[col_key])
                        im_metadata[sanitised_col_key] = row[col_key]
                    trigger_number = str(row["trigger#"])
                    if not no_metadata:
                        with open(target + "_TN" + trigger_number + ".json", "w") as f:
                            json.dump(im_metadata, f, ensure_ascii=False)
                    image.save(target + "_TN" + trigger_number + ".tiff", "TIFF")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument("-x", "--exclude-metadata", type=str, required=False, help="Set path to raw IFCB directory (adc, hdr, and roi files).")
    parser.add_argument("-x", "--exclude-metadata", action="store_true", required=False, help="don't add metadata to resulting image files.")
    parser.add_argument("file", nargs='+', help="any number of .adc, .hdr or .roi files")

    args = parser.parse_args()

    in_files = args.file
    targets = []

    for in_file in in_files:
        in_file_s = os.path.splitext(in_file)
        if in_file_s[1] == ".adc" or in_file_s[1] == ".hdr" or in_file_s[1] == ".roi":
            targets.append(in_file_s[0])
        else:
            print("invalid extension \"" + in_file_s[1][1:] + "\" in file \"" + in_file + "\", ignoring")

    # Get rid of duplicates
    targets = list(set(targets))

    for target in targets:
        extract_ifcb_images(target, no_metadata = args.exclude_metadata)

