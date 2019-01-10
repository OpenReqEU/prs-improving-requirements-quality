FROM python:3.6

COPY . .

RUN pip install -r requirements.txt

RUN python -m nltk.downloader wordnet

RUN python -m spacy download en

CMD [ "python", "./starter.py"]