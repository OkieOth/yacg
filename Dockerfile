FROM python:3.8-slim-buster

RUN pip install pipenv

WORKDIR /yacg

ADD yacg.py yacg.py
ADD incrementVersion.py incrementVersion.py
ADD modelToJson.py modelToJson.py
ADD modelToYaml.py modelToYaml.py
ADD version.txt version.txt
ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock
COPY yacg yacg/

#RUN cd /yacg && \
#    pipenv --python 3.8 && \
#    pipenv --three install --system

RUN pipenv lock -r > requirements.txt
RUN pip install -r requirements.txt

WORKDIR /yacg

ENTRYPOINT [ "python3", "yacg.py"]