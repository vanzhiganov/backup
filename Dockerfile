FROM ubuntu
RUN apt-get update
WORKDIR /tmp/
COPY . .
CMD ["python backup.py --help"]