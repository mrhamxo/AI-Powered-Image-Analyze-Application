# use python 3.11 base image
FROM python:3.11-slim

# set the working directory
WORKDIR /app    

# copy the requirements file and install dependancies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the application code
COPY . .

# expose the application port
EXPOSE 8000

# command to run FastApi application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
