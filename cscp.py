#!/usr/bin/env python3.10

from genericpath import exists
import os
import time

from argparse import ArgumentParser
from io import TextIOWrapper

def copy(sources: list[str], dest: str, csize: int) -> bool:
    dest: str=os.path.realpath(dest)

    for source in sources:
        source: str=os.path.realpath(source)

        if (os.path.isdir(source)):
            sitems: list=list(map(lambda item: os.path.join(source, item), os.listdir(source)))

            os.makedirs(dest, exist_ok=True)
            copy(sitems, dest, csize)
        else:
            if (os.path.islink(source)):
                link_dest: str=os.readlink(source)
                os.symlink(link_dest, os.path.join(dest, os.path.basename(source)), False)
            else:
                with open(source,'rb') as sourcef:
                    chunk: bytes=sourcef.read(csize)

                    if (os.path.exists(dest) and os.path.isdir(dest)):
                        dest: str=os.path.join(dest, os.path.basename(source))

                    destf: TextIOWrapper=open(dest,"wb")

                    while (chunk):
                        destf.write(chunk)
                        time.sleep(1)
                        chunk = sourcef.read(csize)

                    destf.close()

    return True

def main() -> int:
    program_ap: ArgumentParser=ArgumentParser()

    program_ap.add_argument("-c", "--chunk_size", action="store", type=int, nargs=1, default=[(1024*1024)])
    program_ap.add_argument("source", metavar="SOURCE", action="store", type=str, nargs="+")
    program_ap.add_argument("dest", action="store", type=str, nargs=1)
    args: object = program_ap.parse_args()

    return int(copy(args.source, args.dest[0], args.chunk_size[0]))

if __name__ == "__main__":
    exit(main())