FROM python:3.11.2-alpine3.17
LABEL maintainer="metalbrain.net"

ENV PYTHONUNBUFFERED=1
ENV SURPRISE_DATA_FOLDER=/app/.surprise_data

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
COPY ./app/collaborative_model.pkl /app/collaborative_model.pkl
COPY ./app/content_model.pkl /app/content_model.pkl
WORKDIR /app

EXPOSE 8000

ARG DEV=true

RUN apk add --no-cache curl tar xz && \
  curl -o node.tar.xz https://nodejs.org/dist/v20.17.0/node-v20.17.0-linux-x64.tar.xz && \
  mkdir -p /usr/local/lib/nodejs && \
  tar -xJf node.tar.xz -C /usr/local/lib/nodejs && \
  ln -s /usr/local/lib/nodejs/node-v20.17.0-linux-x64/bin/node /usr/local/bin/node && \
  ln -s /usr/local/lib/nodejs/node-v20.17.0-linux-x64/bin/npm /usr/local/bin/npm && \
  ln -s /usr/local/lib/nodejs/node-v20.17.0-linux-x64/bin/npx /usr/local/bin/npx

RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu


RUN python -m venv /py && \
  /py/bin/pip install --upgrade pip && \
  /py/bin/pip install "numpy<2" cython && \
  apk add --update --no-cache libgomp && \
  apk add --update --no-cache libstdc++ && \
  apk add --update --no-cache postgresql-client jpeg-dev && \
  apk add --update --no-cache --virtual .tmp-build-deps \
  build-base postgresql-dev musl-dev zlib zlib-dev && \
  /py/bin/pip install -r /tmp/requirements.txt && \
  if [ "$DEV" = "true" ]; \
  then /py/bin/pip install -r /tmp/requirements.dev.txt; \
  fi && \
  rm -rf /tmp && \
  apk del .tmp-build-deps && \
  adduser \
  --disabled-password \
  --no-create-home \
  django-user && \
  mkdir -p /vol/web/media && \
  mkdir -p /vol/web/static && \
  mkdir -p /app/.surprise_data && \
  chown -R django-user:django-user /vol && \
  chmod -R 755 /vol && \
  chown -R django-user:django-user /app/.surprise_data && \
  chmod -R 755 /app/.surprise_data

ENV PATH="/py/bin:$PATH"

USER django-user


