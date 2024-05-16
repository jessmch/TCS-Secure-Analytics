#!/bin/bash

pip install pandas pandasai langchain langchain_experimental cryptography
curl -fsSL https://ollama.com/install.sh | sh
ollama run mistral