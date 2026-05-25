# use slim docker pythin image to keep the image small
FROM python:3.11-slim

# dont run as root user 
RUN useradd -m appuser 

WORKDIR /app

# install dependencies first 
COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt

# copy application code 
COPY app.py  . 

# switch to non-root user 
USER appuser 

# expose the port flask runs on
EXPOSE 5000

# use unicorn instead of flask dev server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]