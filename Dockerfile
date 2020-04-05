FROM python:3.8-slim-buster

RUN pip install pipenv

ADD yacg.py /yacg/
ADD Pipfile /yacg/
ADD Pipfile.lock /yacg/
COPY yacg /yacg/yacg/

RUN cd /yacg && \
    pipenv --python 3.8 && \
    pipenv --three install

WORKDIR /yacg

ENTRYPOINT [ "pipenv", "run", "python3", "yacg.py"]