FROM python:3.11.8

WORKDIR /app

COPY ./requirements.txt .

RUN python3 -m pip install --upgrade pip

RUN python3 -m pip install -r requirements.txt

ENV PYTHONPATH=/app/code

EXPOSE 8501

CMD ["streamlit", "run", "Start.py"]

# docker build -t tokmanni .
# HUOM! W11
# docker run -it -v "/$(pwd):/app" -p 8501:8501 tokmanni bash 
# Linux ehkä myös iOs
# docker run -it -v `pwd`:/app -p 8501:8501 tokmanni bash   
# http://localhost:8501/
