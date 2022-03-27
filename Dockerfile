FROM alpine:latest
RUN mkdir /workspace
WORKDIR /workspace
COPY tiddlywiki.html /workspace/index.html
COPY server-wiki.py /server.py
RUN apk add --no-cache python3
CMD ["python3","/server.py"]
EXPOSE 88
