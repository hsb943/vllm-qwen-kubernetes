FROM vllm/vllm-openai:latest

WORKDIR /app
COPY server.py /app/server.py

EXPOSE 8080

ENTRYPOINT ["python3", "/app/server.py"]

