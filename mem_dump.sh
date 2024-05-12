#!/bin/bash

pid=$(pgrep -f "python crypt.py")

gcore -o memdump.core $pid >/dev/null 2>&1
echo $(strings memdump.core.$pid | grep "sensitive information")
