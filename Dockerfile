FROM python:3.8

ENTRYPOINT /app

COPY . .

#RUN python -m venv pythonLogBonk

#RUN source pythonLogBonk/bin/activate

#RUN ["/bin/bash", "-c", "source pythonLogBonk/bin/activate"]

RUN pip install schedule

RUN python3 ./server/server.py

