#!/bin/bash

pid=$(pgrep -f "nitro-cli run-enclave --cpu-count 2 --memory 9000 --enclave-cid 16 --eif-path tcs-black-box.eif --debug-mode")

gcore -o memdump.core $pid >/dev/null 2>&1
echo $(strings memdump.core.$pid | grep "Classification report:")
echo $(strings memdump.core.$pid | grep "Confusion matrix:")
echo $(strings memdump.core.$pid | grep "Query:")
echo $(strings memdump.core.$pid | grep "Response:")