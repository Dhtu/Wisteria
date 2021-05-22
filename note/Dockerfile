FROM archlinux
RUN pacman -Syu --noconfirm&& \
pacman -S --noconfirm bpf bcc bcc-tools python-bcc python-pip inetutils vim thrift python-thrift && \
pip3 install kafka-python prometheus_client
