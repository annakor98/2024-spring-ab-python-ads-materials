# Семинар 27 февраля 2024 г.
## Запуск Airflow в Kind

1. Подготовим кластер (см. [kind-cluster.yaml](../sem_20240319/kind-cluster.yaml)):
```shell
kind create cluster --name airflow-cluster --config kind-cluster.yaml
```

2. Установим ```Airflow```:
```shell
kubectl create namespace airflow
helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm install airflow apache-airflow/airflow --namespace airflow --debug
```

3. Для доступа к ```Airflow UI```:
```shell
kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow
```

4. Получим файл с конфигами:
```shell
helm show values apache-airflow/airflow > values.yaml
```

5. Конфигурируем ```Airflow```, для этого в `values.yaml` отредактируем следующие параметры:
```yaml
executor: "KubernetesExecutor"
```
Укажем репозиторий и папку с DAG'ами:
```yaml
  gitSync:
    enabled: true

    # git repo clone url
    # ssh example: git@github.com:apache/airflow.git
    # https example: https://github.com/apache/airflow.git
    repo: https://github.com/username/reponame.git
    branch: main
    rev: HEAD
    depth: 1
    # the number of consecutive failures allowed before aborting
    maxFailures: 0
    # subpath within the repo where dags are located
    # should be "" if dags are at repo root
    subPath: "dags_folder_path"
```

6. Соберем образ с необходимыми библиотками:
<h5 a><strong><code>Dockerfile</code></strong></h5>

``` dockerfile
FROM apache/airflow:2.8.1
COPY requirements.txt .
RUN pip install -r requirements.txt
```

```shell
docker build -t airflow-custom:1.0.0 .
```

Загрузим его на кластер:
```shell
kind load docker-image airflow-custom:1.0.0 --name airflow-cluster
```

И отредактируем ```values.yaml```:
```yaml
# Default airflow repository -- overridden by all the specific images below
defaultAirflowRepository: airflow-custom

# Default airflow tag to deploy
defaultAirflowTag: "1.0.0"
```

7. Применим изменения:
```shell
helm upgrade --install airflow apache-airflow -n airflow -f values.yaml --debuf
```