FROM python:3.8.16-slim

RUN useradd -m thesoft
WORKDIR /home/thesoft
COPY Pipfile Pipfile.lock README.md LICENSE .
COPY the_soft ./the_soft
RUN chown -R thesoft:thesoft /home/thesoft
USER thesoft

ENV PATH="$PATH:/home/thesoft/.local/bin"
RUN pip install pipenv
RUN pipenv install --system --deploy

ENTRYPOINT ["python", "the_soft"]
