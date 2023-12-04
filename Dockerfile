# Version of Python
FROM python:3.9
ADD main.py .

# Setup Working Directory
WORKDIR /marilearn

# Copy requirement.txt into working directory 
COPY ./requirements.txt /marilearn/requirements.txt

# Install all the dependency
RUN pip install --no-cache-dir --upgrade -r /marilearn/requirements.txt

# Copy code into working directory
COPY . /marilearn


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]