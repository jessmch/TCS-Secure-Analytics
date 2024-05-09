#!/bin/bash

pid=$(pgrep -f "python crypt.py")

gcore -o memdump.core $pid >/dev/null 2>&1
echo $(strings memdump.bin.$pid | grep "sensitive information")
