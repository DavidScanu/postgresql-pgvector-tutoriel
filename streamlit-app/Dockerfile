FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /streamlit-app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD streamlit run Detection.py --server.port=$PORT --server.address=0.0.0.0