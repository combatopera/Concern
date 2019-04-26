FROM python
SHELL ["bash", "-c"]
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install --assume-yes screen vim portaudio19-dev && \
    pip install pyparsing numpy cython colorlog pyaudio
ADD await-sigterm /usr/local/bin
ENV MINICONDA3_HOME /usr/local
ARG EUID
ARG EGID
ARG USERNAME
ARG GROUPNAME
RUN groupadd --gid $EGID $GROUPNAME && useradd --gid $EGID --uid $EUID --groups audio $USERNAME
ARG GENERATION
ENV CONCERN_GENERATION $GENERATION
RUN for spec in aridity pyven pym2149 pyrbo@py3 nativecommon diapyr outjack mynblep@py3 FoxDot system splut Concern; \
        do IFS=@ read project branch <<<$spec && \
        git clone --branch ${branch:-master} --single-branch https://github.com/combatopera/$project /opt/$project; \
    done && \
    find /opt -mindepth 1 -type d -exec chmod 1777 '{}' + && \
    ln -s /opt/pyven/pyven /usr/local/bin
USER $EUID
CMD ["await-sigterm"]
