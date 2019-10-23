FROM python:3.6

COPY . .
# .dockerignore lists what should not be copied

RUN pip install -r requirements.txt

RUN python -m nltk.downloader wordnet
RUN python -m nltk.downloader punkt

RUN python -m spacy download en


CMD [ "python", "./starter.py"]