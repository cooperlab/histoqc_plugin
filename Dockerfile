FROM python:3.9
MAINTAINER Lee Cooper <lee.cooper@northwestern.edu>

RUN pip install --pre girder-slicer-cli-web
RUN pip install girder-client

COPY . $PWD
ENTRYPOINT ["python", "./cli_list.py"]