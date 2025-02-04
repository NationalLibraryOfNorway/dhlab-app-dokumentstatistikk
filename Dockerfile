FROM python:3.12
        EXPOSE 8501
        WORKDIR /document_statistics.py
        COPY requirements.txt ./requirements.txt
        RUN pip3 install -r requirements.txt
        COPY . .
        CMD streamlit run document_statistics.py --server.baseUrlPath /dokumentstatistikk

