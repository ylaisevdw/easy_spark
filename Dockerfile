FROM python:3.8

RUN pip3 install --upgrade Cython
RUN apt-get update && apt-get install openjdk-11-jre-headless -y
COPY ./requirements.txt /
RUN pip3 install -r requirements.txt
COPY ./start.sh /
COPY ./app /app
ADD ./app/input_file /app/input_file
RUN chmod +x /start.sh
ENTRYPOINT [ "/start.sh" ]
CMD ["python", "/app/gui.py"]



