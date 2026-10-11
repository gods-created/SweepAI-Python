FROM python:3.14-slim 

COPY . /app 

WORKDIR /app 

EXPOSE 8001 

RUN apt-get update 
RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt
RUN chmod +x /app/entrypoint.sh

STOPSIGNAL SIGQUIT

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD NONE

ENTRYPOINT [ "/app/entrypoint.sh" ]