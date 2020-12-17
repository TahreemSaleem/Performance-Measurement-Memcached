FROM ubuntu:16.04
      
MAINTAINER Your name <tahreem.saleem@mailbox.tu-dresden.de>


RUN apt-get update
RUN apt-get upgrade -y

#ssh setup
RUN apt-get install -y openssh-server sudo
ENV git_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDcFj9AJ0yx2NswwEKPFQZqpiYZ8Mzk1LlRNatsVQqUfaDoQTKewuHRpp5jREB9RIMPczgFPDZSOBQ+mV8u5qJScmOcB8rhaF0GZkF1KIgHSNj8VqDNZWP52m1+NxSJetp6Opu3zTzkoZt9uo4HHeVZseTfN0UkxSjcWKYPX7+rOrvMhIxxKB9bR7UjmMkmoMfzP8UVkmc4MxIOo+RW9OM9GFselGN9JTYceZW8xhWNH2ENXQNWE5a807vP6kaKWp5bQ/c7NpISvTAO5UaVD26IRrtqea//MiUORjbXX+dEpFZuN6fRMh+zemerQ9rDHcgxRMacGZxBUjIRCa92zSr3 gitlab-runner@sep"
ENV local_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDM84P1ZJyVdOr68Nzigm+lYkom56VO7ysmnlAB2fOyzxgLwNQssoA72lFiRN+GA8VZWePuSA0PLehD4e4pp6/wB8DNeXHg9piomFE10rwAca7OE6AyGeBCkO65Ko6rzpU/KZWibMBv35YiJt4UbNQYle6WgidZaq9RE01gbxtWjA4WKENZoHLneVWyOoaBpTReO2TNQ6T7chmDIRT0TMCCnuYPIVf5ZnkYW+be0Ea0/nG41MEXfPF819Eg/De9QXiblDF/Wav51Qt/GKhHiSVD1Ris2XzMtkplCkJAgvTMT4b30FPyQt0SZzRczh1ICzNCW3qMve5bL2UjIEu2hFGT root@localhost"
ENV container_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDYRWv7iR0VeVXu3ktkzcl3zV5KDl8r0s+vHREgJ6bj1tTfcIdbovese0YdfmTc4vvWJQRrvFktS7T5Bmo3/0+M46BIBXojcOkQ4tRXDvyCfrLGjumewix2WowaOPh5FJv84FPFtvNaLSrucz4SVDXkB6UvnadRhPe9yZDX+cYino2diqJnU4UrpmDhnMl8cbtaVWH6HVZL7mxK5qjod0MjJM4+WIniOExxg8CIpACXZQhGGoI9bwRdCBdMX78i/rmhOAbJ4u2rVx5HhYQs0NCUDrM9Y+0Z+U6l7EPoD52S0w1ZVzfrUhuL9v6ul8qmpCV9/tQzcvZcobtn7InpzFm7 ts@ts-Laptop"
#memcached prereq
RUN apt-get install -y gcc make wget
RUN wget https://github.com/libevent/libevent/releases/download/release-2.1.8-stable/libevent-2.1.8-stable.tar.gz
RUN tar -zxf libevent-2.1.8-stable.tar.gz
RUN cd /libevent-2.1.8-stable && ./configure -prefix=/usr && make && make install
RUN cd /
##memcached installation
ENV VERSION=1.4.33
RUN wget http://www.memcached.org/files/memcached-$VERSION.tar.gz
RUN tar -zxf memcached-$VERSION.tar.gz
RUN cd memcached-$VERSION && ./configure && make && make install
#RUN ln -s /usr/lib/libevent-2.1.so.6 /usr/lib64/libevent-2.1.so.6
RUN rm -f /memcached-$VERSION.tar.gz

EXPOSE 11211

RUN mkdir /app
COPY entrypoint.sh /app
RUN chmod +x /app/entrypoint.sh



RUN mkdir -p /home/ubuntu/.ssh

RUN echo "$local_key\n" > /home/ubuntu/.ssh/authorized_keys
RUN echo "$gitlab_key\n" >> /home/ubuntu/.ssh/authorized_keys
RUN echo "$container_key" >> /home/ubuntu/.ssh/authorized_keys
RUN chmod 700 /home/ubuntu/.ssh/authorized_keys

COPY sshd_config /home/ubuntu/.ssh/sshd_config
RUN chmod 700 /home/ubuntu/.ssh/sshd_config



# Setup the default user.


RUN service ssh start


RUN useradd -ms /bin/bash -g root -G sudo -u 1000 ubuntu
RUN usermod -aG sudo ubuntu
RUN echo 'ubuntu:ubuntu' | chpasswd

RUN cp /etc/ssh /home/ubuntu/ssh -r
RUN chmod 600 /home/ubuntu/ssh/* && ls /home/ubuntu/ssh/
RUN chown -R ubuntu /home/ubuntu/ssh
RUN chown -R ubuntu /home/ubuntu/

WORKDIR /home/ubuntu

EXPOSE 2000

#CMD ["/usr/sbin/sshd","-D"]
#RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 Ubuntu
#
#RUN  echo 'test:test' | chpasswd
#
##non root user
#RUN useradd -u 1000 Ubuntu
## Change to non-root privilege
#USER Ubuntu
RUN chown -R ubuntu /etc/ssh
USER ubuntu


#have to search how to run ssh and memecached together
ENTRYPOINT ["/app/entrypoint.sh"]