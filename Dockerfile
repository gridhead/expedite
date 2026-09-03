FROM fedora:44

LABEL maintainer "Akashdeep Dhar <t0xic0der@fedoraproject.org>"

EXPOSE 6969

ENV PYTHONBUFFERED=1

RUN dnf install python3-pip --assumeyes && dnf clean all --assumeyes
RUN pip3 install --upgrade expedite==0.1.0

ENTRYPOINT ["ed-server"]
CMD ["--addr", "0.0.0.0", "--port", "6969"]
