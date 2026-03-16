FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables (set at runtime, not build time)
ENV LLM_PROVIDER=gemini
ENV OPENAI_API_KEY=""
ENV GEMINI_API_KEY=""
ENV HUGGINGFACE_API_KEY=""
ENV OPENAI_MODEL=gpt-4o
ENV GEMINI_MODEL=gemini-1.5-flash
ENV DEFAULT_MEMORY_LIMIT=5
ENV MAX_AGENTS=10

# Run the application
CMD ["python", "main.py"]
