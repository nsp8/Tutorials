FROM python:3.12
WORKDIR /app
COPY ./requirements.txt /user_crud/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./user_crud /user_crud/app

CMD ["fastapi", "run", "app/main.py", "--port", "80", "--workers", "4"]
