# Use the official Python runtime image
FROM python:3.13  
 
# Create the app directory
RUN mkdir /app
 
# Set the working directory inside the container
WORKDIR /app
 
# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 

# ubstall odbc shared objects for azure sql to work
RUN apt update -y 
RUN apt install unixodbc -y 

# Upgrade pip
RUN pip install --upgrade pip 
 
# Copy the Django project  and install dependencies
COPY requirements.txt  /app/
 
# run this command to install all dependencies 
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the Django project to the container
COPY . .
 
# Expose the Django port
EXPOSE 8000

##RUN apt-get update -y
##RUN apt install unixodbc -y

#HEALTHCHECK --interval=5m --timeout=3s --retries=3 CMD curl http://localhost:8000/admin || exit 1
 
# Run Django’s development server
CMD ["sh", "docker-entrypoint.sh"]