FROM ubuntu:20.04


WORKDIR /app



RUN apt-get update && apt-get install -y apt-transport-https ffmpeg libsm6 libxext6 poppler-utils
RUN apt-get install -y python3-pip
RUN apt-get install python3-dev


RUN apt-get install -y build-essential 
RUN apt-get install -y libssl-dev 
RUN apt-get install -y libffi-dev
RUN apt install libpq-dev gcc

RUN cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 --no-cache-dir install --upgrade pip \
  && rm -rf /var/lib/apt/lists/*


# copy project
ENV PATH=/virtualenv/bin:$PATH
RUN pip install virtualenv 
# RUN apt install -y redis
RUN mkdir virtualenv 
RUN virtualenv /virtualenv

COPY requirements.txt requirements.txt


RUN pip install -r requirements.txt
RUN pip install 'requests[socks]'
COPY . .
RUN python manage.py collectstatic --noinput
# RUN python manage.py makemigrations


