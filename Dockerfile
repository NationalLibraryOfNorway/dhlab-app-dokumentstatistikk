FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
        ENV PORT=8501
        EXPOSE $PORT
        WORKDIR /document_statistics.py

        COPY requirements.txt ./requirements.txt
        RUN uv pip install          \
            -r requirements.txt     \
            --system                \
            --compile-bytecode

        COPY document_statistics.py DHlab_logo_web_en_black.png  ./

        # Warm up caches
        RUN python -c 'import streamlit, pandas, dhlab, matplotlib, requests'
        RUN timeout 5s streamlit run document_statistics.py; exit 0

        CMD streamlit run document_statistics.py        \
            --server.port ${PORT}                       \
            --server.baseUrlPath /dokumentstatistikk    \
            --browser.gatherUsageStats false

