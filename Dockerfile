FROM python:3

WORKDIR /app/verd_andi

ENV DEBUG=False DB=ppp_db

ADD requirements.txt /app/

RUN pip install --no-cache-dir -r ../requirements.txt && \
    rm -rf /var/lib/apt/lists/*

COPY src/verd_andi /app/verd_andi
COPY src/static_in_env /app/static_in_env

EXPOSE 8000

CMD ["gunicorn", "--bind","0.0.0.0","verd_andi.wsgi"]
