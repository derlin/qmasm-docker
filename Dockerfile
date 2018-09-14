FROM python:2.7

RUN apt update && apt install -y less vim cmake
RUN pip install --upgrade pip

RUN git clone https://github.com/dwavesystems/qbsolv.git
RUN mkdir /qbsolv/build && cd /qbsolv/build && cmake .. && make && cp qbsolv /usr/local/bin


RUN git clone https://github.com/lanl/qmasm.git
RUN cd qmasm && python setup.py install
RUN pip install dwave-qbsolv

RUN pip install cherrypy
RUN mkdir /rest
COPY server.py /rest
EXPOSE 80

RUN mkdir /app 
WORKDIR /app 

CMD [ "python", "/rest/server.py" ]