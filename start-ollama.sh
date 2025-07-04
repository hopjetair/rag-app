FROM ollama/ollama:latest

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Create directory for models
RUN mkdir -p /root/.ollama

# Copy startup script
COPY start-ollama.sh /start-ollama.sh
RUN chmod +x /start-ollama.sh

EXPOSE 11434

CMD ["/start-ollama.sh"]