FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
        ENV PORT=8501
        EXPOSE $PORT
        WORKDIR /document_statistics.py

        COPY requirements.txt ./requirements.txt
        RUN uv pip install --system -r requirements.txt

        COPY document_statistics.py DHlab_logo_web_en_black.png  .
        CMD streamlit run document_statistics.py --server.port ${PORT} --server.baseUrlPath /dokumentstatistikk

