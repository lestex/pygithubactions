FROM python:3.10 as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt upgrade -y

WORKDIR /app
COPY . /app/

# install app
RUN pip install .

ENV HOME="/home/nonadmin"
RUN groupadd -r -g 1001 nonadmin && useradd -r -d $HOME -u 1001 -g nonadmin nonadmin
RUN mkdir -p $HOME
RUN chown nonadmin $HOME
USER nonadmin

CMD [ "python", "-V"]
