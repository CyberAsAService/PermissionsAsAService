#FROM metasploitframework/metasploit-framework:latest
#FROM ubuntu:latest
FROM kalilinux/kali:latest
# install python dependencies
RUN apt update && \
        apt-get -y install python3 git python3-setuptools python3-pip libevent-dev python3-dev build-essential curl winexe

# install metasploit
RUN curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && \
  chmod 755 msfinstall && \
  ./msfinstall
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY . .
RUN chmod +x *.sh 
EXPOSE 5000
ENTRYPOINT ["./docker-entrypoint.sh"]
#CMD ["webserver"]
