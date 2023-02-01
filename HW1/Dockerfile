FROM scratch
ADD ubuntu-focal-oci-arm64-root.tar.gz /

RUN apt-get update
RUN apt-get install -y sysbench 
RUN apt-get install -y linux-tools-common linux-tools-generic

COPY experiment1.sh /root/experiment1.sh
COPY experiment2.sh /root/experiment2.sh


CMD /bin/bash /root/experiment1.sh && /bin/bash /root/experiment2.sh &&  tail -f /dev/null
