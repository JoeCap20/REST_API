FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

#How to run Docker from terminal
#docker -run -p 5005:5000 rest-apis-flask-python
#-d before -p will run it in the background