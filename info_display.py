import os
from pathlib import Path
import cv2
import re
from datetime import timedelta, datetime
from tabulate import tabulate
import argparse as ap
import yaml


def check_size(path: str) -> int:
    return os.path.getsize(path)


def check_duration(path: str) -> int:
    vc = cv2.VideoCapture(path)
    if not vc.isOpened():
        return 0

    return int(vc.get(cv2.CAP_PROP_FRAME_COUNT)) / int(vc.get(cv2.CAP_PROP_FPS))


DATA_UNITS_BI = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'EiB']
DATA_UNITS_DEC = ['B', 'KB', 'MB', 'GB', 'TB', 'EB']


def convert_size(size: int, use_binary_unit=True) -> str:
    uplift_count = 0
    s = size
    upper_limit = 1024 if use_binary_unit else 1000
    units = DATA_UNITS_BI if use_binary_unit else DATA_UNITS_DEC
    uplift_limit = len(units)

    while s > upper_limit and uplift_count < uplift_limit:
        s /= upper_limit
        uplift_count += 1

    return "{:.2f} {}".format(s, units[uplift_count])


def convert_duration(duration: int) -> str:
    return str(timedelta(seconds=duration))


def update_progressbar(progress, length=40):
    progress = min(progress, 1)
    progress = max(progress, 0)

    inner_width = length - 7
    step = int(inner_width * progress)
    remain = inner_width - step

    print(
        "\r[{}{}] {:3}%"
        .format('#' * step, ' ' * remain, int(progress * 100)),
        end=''
    )


def print_stat(columns: list, display_columns: list, data, additional_info=dict()):
    dc_len, c_len = len(display_columns), len(columns)
    if dc_len < c_len:
        for item in columns[dc_len:]:
            display_columns.append(item)

    tb = dict()
    for dc in display_columns:
        tb[dc] = []

    for item in data:
        for i, col in enumerate(columns):
            tb[display_columns[i]].append(item[col])

    for entry in additional_info.items():
        print(f"{entry[0]}:\t{entry[1]}")

    print(tabulate(tb, headers=display_columns, tablefmt='pretty'))


def save_stat(summary, details, out_dir):
    cur_time = datetime.now().strftime(r"%Y-%m-%d_%H-%M-%S")
    with open(Path(out_dir) / f"info_display_{cur_time}.yaml", 'w+') as f:
        f.write(yaml.dump({
            "summary": summary,
            "files": details,
        }))


def main(args):
    path = args.dir
    result_path = args.stat_dir
    pattern = args.pattern
    exts = args.ext
    show_duration = args.show_duration

    spl = '-' * 20
    print(spl)
    print('INFODISPLAY V0.01')
    print(spl)

    print("Initializing... ", end='')
    stat = []

    iter_d = [*Path(path).iterdir()]
    total = len(iter_d)
    completed = 0
    print("done")
    print("Processing...")

    for item in iter_d:
        completed += 1
        update_progressbar(completed / total)

        if not item.is_file():
            continue

        s_ext = item.name.split('.')[-1]
        matched = False
        for ext in exts:
            if s_ext == ext:
                matched = True
                break

        if not matched:
            continue

        if pattern and not re.match(pattern, item.name):
            continue

        path_str = str(item)

        if show_duration:
            try:
                duration = check_duration(path_str)
            except:
                duration = 0
        else:
            duration = 0

        stat.append({
            "file": item.name,
            "size": check_size(path_str),
            "duration": duration,
        })

    print()
    print("done")

    print("Constructing data... ", end='')

    display_columns = ['File', 'Size', 'Duration']
    columns = ['file', 'size', 'duration']

    rendering_stat = []

    total_size = 0
    total_duration = 0

    for item in stat:
        r_item = {
            'file': item['file'],
            'size': convert_size(item['size']),
            'duration': convert_duration(item['duration']),
        }
        rendering_stat.append(r_item)

        total_size += item['size']
        total_duration += item['duration']

    summary = {
        "Total size": convert_size(total_size),
        "Total duration": convert_duration(total_duration),
    }

    print('done')

    print(spl)
    print("Statistic")
    print(spl)
    print_stat(columns, display_columns,
               rendering_stat, additional_info=summary)

    if result_path:
        save_stat(summary, rendering_stat, result_path)


if __name__ == '__main__':
    parser = ap.ArgumentParser()
    parser.add_argument("-d", "--dir", default=".", type=str,
                        help="Root directory to scan (Default: %(default)s)")
    parser.add_argument("-P", "--pattern", type=str,
                        help="Search pattern (Regular Expression)")
    parser.add_argument("-e", "--ext", "--extension", nargs='*', action='extend', default=[],
                        help="Extensions for scanning")
    parser.add_argument("-s", "--stat-dir",
                        help="Directory for saving output statistic file")
    parser.add_argument('-D', "--show-duration", action='store_true',
                        help="Show duration of files (Audio and video only)")
    main(parser.parse_args())
