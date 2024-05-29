#!/bin/bash

printf "Starting Ollama server"

ollama serve &
ollama list
ollama run mistral