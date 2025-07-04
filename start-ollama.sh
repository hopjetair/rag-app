#!/bin/bash
set -e

echo "Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

echo "Waiting for Ollama to be ready..."
sleep 10

echo "Pulling Mistral model..."
ollama pull mistral

echo "Ollama is ready!"
wait $OLLAMA_PID