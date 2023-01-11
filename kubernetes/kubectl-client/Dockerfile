FROM rockylinux:8
COPY kubernetes.repo /etc/yum.repos.d/kubernetes.repo
COPY kubectl.bash /etc/bash_completion.d/kubectl.bash
RUN yum -y install kubectl vim git bash-completion
CMD while true; do sleep 3600; done