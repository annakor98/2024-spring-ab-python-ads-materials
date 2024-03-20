# Семинар 19 марта 2024 г.
## MLServer

1. Обучим и сохраним модель с помощью `joblib` (см. [train.py](train.py)).
2. Подготовим inference модели, для этого завернем ее в класс (наследуемся от `mlserver.MLModel`, см. [inference.py](inference.py))
3. Подготовим конфиги для `mlserver`:

<h5 a><strong><code>settings.json</code></strong></h5>

``` json
{
    "debug": "true"
}
```
<h5 a><strong><code>model_settings.json</code></strong></h5>

``` json
{
  "name": "iris-predictor",
  "implementation": "inference.IrisPredictor",
  "parameters": {
    "uri": "./model.joblib"
  }
}
```
4. Запустим сервер:
```shell
mlserver start .
```
Для тестирования используем POST на `http://localhost:8080/v2/models/iris-predictor/infer` (см. [test.py](test.py))

5. Подготовим `requirements.txt` (указывать `mlserver` не нужно), например:
<h5 a><strong><code>requirements.txt</code></strong></h5>

```text
scikit-learn==1.4.1.post1
```
6. Соберем образ с помощью `mlserver`:
```shell
mlserver build . -t annakor98/iris_seldon
```
и запушим его на `DockerHub`. При тестировании не забываем указать `--ports 9000:9000` в `docker run`.

## Seldon Core

1. Подготовим кластер:
```shell
kind create cluster --name seldon-cluster --config kind-cluster.yaml --image=kindest/node:v1.21.1
```

2. Установим `Ambassador`:
```shell
helm repo add datawire https://www.getambassador.io
helm repo update
```
```shell
helm upgrade --install ambassador datawire/ambassador \                                           
  --set image.repository=docker.io/datawire/ambassador \
  --set service.type=ClusterIP \
  --set replicaCount=1 \
  --set crds.keep=false \
  --set enableAES=false \
  --create-namespace \
  --namespace ambassador
```

3. Установим `Seldon Core`:
```shell
helm install seldon-core seldon-core-operator \                                                   
    --repo https://storage.googleapis.com/seldon-charts \
    --set usageMetrics.enabled=true \
    --set ambassador.enabled=true \
    --create-namespace \
    --namespace seldon-system \
    --version 1.15
```
4. Подготовим `SeldonDeployment` (см. [deployment.yaml](deployment.yaml)):
```shell
kubectl create -f deployment.yaml
```
5. Для тестирования:
```shell
kubectl port-forward svc/iris-predictor-iris-predictor-iris-predictor 9000:9000
```