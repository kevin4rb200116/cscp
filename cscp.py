#!/usr/bin/env python3.9

import os
import time
import sys

from argparse import ArgumentParser
from io import BytesIO

def info(s: str) -> None:
    sys.stdout.write(f"[I]: {s}")
    sys.stdout.write('\n')
    sys.stdout.flush()

def error(s: str) -> None:
    sys.stderr.write(f"[E]: {s}")
    sys.stderr.write('\n')
    sys.stderr.flush()

def copy(sources: list[str], dest: str, csize: int) -> bool:
    for source in sources:
        src_item: str = os.path.realpath(source)
        dst_item: str = os.path.realpath(dest)

        if (os.path.isdir(src_item)):
            sub_src_items: list=list(map(lambda item: os.path.join(src_item, item), os.listdir(src_item)))

            if (os.path.exists(dst_item) and os.path.isdir(dst_item)):
                sub_items_dst: str=os.path.join(dst_item,os.path.basename(src_item))
            else:
                sub_items_dst: str=dst_item

            os.makedirs(sub_items_dst, exist_ok=True)

            copy(sub_src_items, sub_items_dst, csize)
        else:
            if (os.path.exists(dst_item) and os.path.isdir(dst_item)):
                dst_item: str=os.path.join(dst_item, os.path.basename(src_item))
            elif (os.path.exists(dst_item) and not os.path.isdir(dst_item)):
                error(f"{dst_item} arleady exists")
                continue

            if (os.path.islink(src_item)):
                link_dst: str=os.readlink(src_item)
                os.symlink(link_dst, dst_item, False)
            elif os.path.isfile(src_item):
                with open(src_item,'rb') as src_file:
                    with open(dst_item,'wb') as dst_file:
                        chunk: bytes = src_file.read(csize)

                        while (chunk):
                            dst_file.write(chunk)
                            dst_file.flush()
                            time.sleep(1)
                            chunk = src_file.read(csize)

                        dst_file.close()

                    src_file.close()

            info(f"{os.path.basename(src_item)} -> {os.path.dirname(dst_item)}")

    return True

def main() -> int:
    program_ap: ArgumentParser=ArgumentParser()

    program_ap.add_argument("-s", "--chunk-size", action="store", type=int, nargs=1, default=[int(1)])
    program_ap.add_argument("source", metavar="SOURCE", action="store", type=str, nargs="+")
    program_ap.add_argument("dest", action="store", type=str, nargs=1)
    args: object = program_ap.parse_args()

    return int(copy(args.source, args.dest[0], (1024**2)*args.chunk_size[0]))

if __name__ == "__main__":
    exit(main())
