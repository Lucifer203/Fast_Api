FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# CMD [ "alembic","upgrage","head","&&","uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

