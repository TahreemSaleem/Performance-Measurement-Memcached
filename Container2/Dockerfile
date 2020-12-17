FROM ubuntu:16.04
      
MAINTAINER Your name <tahreem.saleem@mailbox.tu-dresden.de>


RUN apt-get update
RUN apt-get upgrade -y

#ssh setup
RUN apt-get install -y openssh-server sudo
ENV git_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDcFj9AJ0yx2NswwEKPFQZqpiYZ8Mzk1LlRNatsVQqUfaDoQTKewuHRpp5jREB9RIMPczgFPDZSOBQ+mV8u5qJScmOcB8rhaF0GZkF1KIgHSNj8VqDNZWP52m1+NxSJetp6Opu3zTzkoZt9uo4HHeVZseTfN0UkxSjcWKYPX7+rOrvMhIxxKB9bR7UjmMkmoMfzP8UVkmc4MxIOo+RW9OM9GFselGN9JTYceZW8xhWNH2ENXQNWE5a807vP6kaKWp5bQ/c7NpISvTAO5UaVD26IRrtqea//MiUORjbXX+dEpFZuN6fRMh+zemerQ9rDHcgxRMacGZxBUjIRCa92zSr3 gitlab-runner@sep"
ENV local_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDM84P1ZJyVdOr68Nzigm+lYkom56VO7ysmnlAB2fOyzxgLwNQssoA72lFiRN+GA8VZWePuSA0PLehD4e4pp6/wB8DNeXHg9piomFE10rwAca7OE6AyGeBCkO65Ko6rzpU/KZWibMBv35YiJt4UbNQYle6WgidZaq9RE01gbxtWjA4WKENZoHLneVWyOoaBpTReO2TNQ6T7chmDIRT0TMCCnuYPIVf5ZnkYW+be0Ea0/nG41MEXfPF819Eg/De9QXiblDF/Wav51Qt/GKhHiSVD1Ris2XzMtkplCkJAgvTMT4b30FPyQt0SZzRczh1ICzNCW3qMve5bL2UjIEu2hFGT root@localhost"
#ENV container_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDYRWv7iR0VeVXu3ktkzcl3zV5KDl8r0s+vHREgJ6bj1tTfcIdbovese0YdfmTc4vvWJQRrvFktS7T5Bmo3/0+M46BIBXojcOkQ4tRXDvyCfrLGjumewix2WowaOPh5FJv84FPFtvNaLSrucz4SVDXkB6UvnadRhPe9yZDX+cYino2diqJnU4UrpmDhnMl8cbtaVWH6HVZL7mxK5qjod0MjJM4+WIniOExxg8CIpACXZQhGGoI9bwRdCBdMX78i/rmhOAbJ4u2rVx5HhYQs0NCUDrM9Y+0Z+U6l7EPoD52S0w1ZVzfrUhuL9v6ul8qmpCV9/tQzcvZcobtn7InpzFm7 ts@ts-Laptop"


RUN mkdir -p /home/ubuntu/.ssh
RUN mkdir -p /root/.ssh
COPY sshcontainerkey /home/ubuntu/.ssh/
RUN echo "$local_key\n" > /home/ubuntu/.ssh/authorized_keys
RUN echo "$gitlab_key\n" >> /home/ubuntu/.ssh/authorized_keys
#RUN echo "$container_key" >> /home/ubuntu/.ssh/authorized_keys
RUN chmod 700 /home/ubuntu/.ssh/authorized_keys
RUN chmod 700 /home/ubuntu/.ssh/sshcontainerkey

#RUN cp /home/ubuntu/.ssh/authorized_keys /root/.ssh/authorized_keys

COPY sshd_config /home/ubuntu/.ssh/sshd_config
RUN chmod 700 /home/ubuntu/.ssh/sshd_config

#install mcperf
RUN apt-get install -y gcc make wget
RUN cd /home/ubuntu
RUN wget https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/twemperf/mcperf-0.1.1.tar.gz
RUN tar zxvf mcperf-0.1.1.tar.gz
RUN cd mcperf-0.1.1 && ./configure && make && make install
RUN rm -f /mcperf-0.1.1.tar.gz

#install R and Dude
RUN apt install -y r-base python git
RUN git clone https://bitbucket.org/db7/dude.git
RUN cd /dude && python setup.py install



RUN service ssh start

# Setup the default user.
RUN useradd -ms /bin/bash -g root -G sudo -u 1000 ubuntu
RUN usermod -aG sudo ubuntu
RUN echo 'ubuntu:ubuntu' | chpasswd

RUN cp /etc/ssh /home/ubuntu/ssh -r
#COPY sshcontainerkey /home/ubuntu/ssh
#RUN chmod 600 /home/ubuntu/ssh/* && ls /home/ubuntu/ssh/
#RUN chown -R ubuntu /home/ubuntu/ssh

#RUN mkdir /home/ubuntu
COPY entrypoint.sh /home/ubuntu/
#RUN chmod +x /home/ubuntu/entrypoint.sh
COPY run.sh graphs.R Benchmark.py Dudefile /home/ubuntu/
#RUN chmod +x /home/ubuntu/run.sh

RUN chmod -R 700 /home/ubuntu/
RUN chown -R ubuntu /home/ubuntu/

WORKDIR /home/ubuntu

EXPOSE 10022

USER ubuntu

ENTRYPOINT ["/home/ubuntu/entrypoint.sh"]