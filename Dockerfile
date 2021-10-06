FROM python:3.8
WORKDIR /
RUN git clone https://github.com/sergitopereira/zscaler_audit_report.git /app/
RUN pip install -r /app/requirements.txt

#ENTRYPOINT [ "python", "/app" ]


