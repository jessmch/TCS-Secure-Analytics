#!/bin/bash

pid=$(pgrep -f "python3 main.py")

gcore -o memdump.core $pid >/dev/null 2>&1
echo $(strings memdump.core.$pid | grep "response:")