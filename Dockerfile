FROM python:3.9.0
EXPOSE 8501
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
RUN chmod +x /app/train_job.sh
RUN /app/train_job.sh
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]