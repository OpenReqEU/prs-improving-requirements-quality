FROM python:3.6

COPY . .
# .dockerignore lists what should not be copied

# Install all Python dependencies requirements
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
# Install NLP library resouces
RUN python -m nltk.downloader wordnet
RUN python -m nltk.downloader punkt
RUN python -m spacy download en
# Start the program
CMD [ "python", "./starter.py"]