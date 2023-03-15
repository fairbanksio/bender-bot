FROM python3.9-alpine
COPY . .
RUN pip install pipenv && pipenv shell && pipenv install
CMD [ "python3", "index.py" ]