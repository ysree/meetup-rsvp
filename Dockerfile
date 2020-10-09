FROM python:3.7-alpine

WORKDIR /app
ADD . /app

RUN apk update \ 
    && apk add --no-cache gcc git python3-dev musl-dev \
    linux-headers libc-dev rsync zsh \ 
    findutils wget util-linux grep \
    libxml2-dev libxslt-dev 
    
RUN pip3 install --upgrade pip
RUN pip3 install aiohttp
RUN pip3 install asyncpg

ADD meetup-rsvp.py /app/meetup-rsvp.py
CMD ["/app/meetup-rsvp.py"]

ENTRYPOINT ["python3"]
