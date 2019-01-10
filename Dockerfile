FROM python:3.6

ADD starter.py /

COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN python -m nltk.downloader wordnet

RUN python -m spacy download en

COPY . .

# different path...
ENV PYTHONPATH /app

CMD [ "python", "./starter.py"]