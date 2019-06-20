FROM python:3.6

COPY . .
# .dockerignore lists what should not be copied

RUN pip install -r requirements.txt

RUN python -m nltk.downloader wordnet

RUN python -m spacy download en

# Currently not functional due to some kind of file location pathing issue
RUN pytest --cov=. --cov-report=xml --cov-config=.coveragerc test_all.py

CMD [ "python", "./starter.py"]