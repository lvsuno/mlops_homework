FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

# Update pip as certain packages (ex: XGBoost) need certain versions of pip
RUN pip install -U pip 
RUN pip install pipenv

#Creates and cd's into the /app directory
WORKDIR /app 
COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY [ "score.py", "./" ]

ENTRYPOINT [ "python", "score.py" ]