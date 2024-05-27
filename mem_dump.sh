#!/bin/bash

pid=$(pgrep -f "python3 main.py")

gcore -o memdump.core $pid >/dev/null 2>&1
echo $(strings memdump.core.$pid | grep "Classification report:")
echo $(strings memdump.core.$pid | grep "Confusion matrix:")
echo $(strings memdump.core.$pid | grep "Query:")
echo $(strings memdump.core.$pid | grep "Response:")