FROM python:3.12-slim

RUN useradd -ms /bin/sh user -us 1000 \
    && mkdir -p /scenario \
    && chown -R user:user /scenario

RUN apt update

COPY ./app /scenario/app
COPY ./requirements.txt /scenario
COPY ./alembic.ini /scenario
COPY ./.pylintrc /scenario

WORKDIR /scenario

RUN pip install uv

RUN uv pip install --system --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

USER user

EXPOSE 8000

CMD ["alembic", "upgread", "head"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]