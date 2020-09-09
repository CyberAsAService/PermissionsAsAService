FROM metasploitframework/metasploit-framework:latest
RUN apk update && \
	apk add --no-cache python3 git py3-setuptools libevent-dev python3-dev build-base	
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY . .
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["PaaS.py"]
