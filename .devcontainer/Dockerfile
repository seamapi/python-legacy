ARG VARIANT="3"

FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

ARG POETRY_VERSION="1.3.1"
ARG POETRY_SRC="https://install.python-poetry.org"

RUN apt-get update \
 && apt-get install -y ca-certificates curl gnupg lsb-release \
 && mkdir -p /etc/apt/keyrings \
 && curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
    | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
 && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu focal stable" \
    | tee /etc/apt/sources.list.d/docker.list > /dev/null \
 && apt-get update \
 && apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

RUN usermod -aG docker vscode

USER vscode
WORKDIR /home/vscode

RUN curl -fsSL -o install-poetry.py "${POETRY_SRC}" \
 && python install-poetry.py --version $POETRY_VERSION \
 && rm install-poetry.py

RUN mkdir -p .config/git \
 && echo ".vscode/*" >> .config/git/ignore \
 && echo "*.code-workspace" >> .config/git/ignore \
 && echo ".history/" >> .config/git/ignore
