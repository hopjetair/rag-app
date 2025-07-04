#!/bin/bash
set -e

echo "=== Starting Ollama Setup ==="

# Set environment variables
export OLLAMA_HOST=0.0.0.0
export OLLAMA_ORIGINS="*"

echo "Starting Ollama server in background..."
ollama serve &
OLLAMA_PID=$!

echo "Waiting for Ollama server to be ready..."
sleep 15

# Wait for Ollama to be responsive
for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo "Ollama server is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "Failed to start Ollama server"
        exit 1
    fi
    echo "Waiting for Ollama server... ($i/30)"
    sleep 2
done

echo "Pulling Mistral model..."
ollama pull mistral

echo "Verifying model is available..."
ollama list

echo "=== Ollama Setup Complete ==="
echo "Ollama server is running with Mistral model"

# Keep the server running
wait $OLLAMA_PID