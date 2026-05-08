FROM frekele/ant

LABEL maintainer="Helmut Konrad Schewe<helmutus@outlook.com>"

ENV PACKAGE=NO_PACKAGE
ENV VERSION=NO_VERSION

ENV MINIMAL=1
ENV LIVE=0

VOLUME /var/src
VOLUME /var/workdir
VOLUME /var/dst

COPY buildit /var/buildit

WORKDIR /var/workdir

ENTRYPOINT /var/buildit
