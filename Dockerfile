
# Base image
FROM python:3.9

# Add non-root user
RUN useradd -m -u 1000 user

# Set working directory inside the user's home
WORKDIR /home/user/app

# Copy requirements and install
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the code
COPY --chown=user . /home/user/app
RUN mkdir -p /home/user/app/uploads && chown -R user:user /home/user/app/uploads
# Create data directory inside user's home (no root needed)
RUN mkdir -p /home/user/app/data

# Switch to non-root user
USER user
 
# Set environment variables
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    APP_PORT=8000

# Expose FastAPI port
# EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
