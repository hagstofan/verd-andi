# FROM docker.hagstofa.local/containers/python:latest
FROM python:3-alpine

WORKDIR /app/verd_andi

ENV DEBUG=False DB=db

ADD requirements.txt /app/

RUN apk add postgresql-dev jpeg-dev zlib-dev build-base python3-dev musl-dev git
ENV LIBRARY_PATH=/lib:/usr/lib
RUN pip3 install --no-cache-dir -r ../requirements.txt && \
	pip3 install flake8 coverage

COPY src/verd_andi /app/verd_andi
COPY src/static_in_env /app/static_in_env
COPY entrypoint.sh /app/verd_andi/entrypoint.sh

# RUN coverage run manage.py test && \
# 	coverage report && \
#	flake8 --exclude manage.py,migrations,django-multiupload .
RUN flake8 --exclude manage.py,migrations,django-multiupload .

EXPOSE 8000

CMD ["sh","/app/verd_andi/entrypoint.sh"]
