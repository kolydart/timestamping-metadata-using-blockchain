#!/bin/bash

FILEURL='https://www.kolydart.gr/download?name=fiction-moments'
HASH=52974bec2f5c33209f60acc1cd1f86ccfbefb39b0cba63162d236bc749c7a2622b5b83fc5d5de9e6a9d500374db2bd1434e3338472a16d113ee352786a0b007a
cd /tmp
curl ${FILEURL} -s -o file_to_check.pdf
echo "${HASH}  file_to_check.pdf" | shasum -a 512 --check - # mac; use " | sha512sum --check" for linux