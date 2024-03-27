# Семинар 26 марта 2024 г.
## Prometheus + Grafana

### Подготовка инфраструктуры

1. Создадим кластер с помощью `Kind`, установим `Ambassador` и `Seldon Core` (см. [tutorial](../sem_20240319/tutorial.md))
2. Установим `Prometheus`:
```shell
helm upgrade --install seldon-monitoring kube-prometheus \        
             --version 8.9.1 \
             --set fullnameOverride=seldon-monitoring \
             --create-namespace \
             --namespace seldon-monitoring \
             --repo https://charts.bitnami.com/bitnami
```
3. Предварительно подготовим файл `values_grafana_local.yaml`, в котором укажем созданный `Prometheus` в качестве источника данных:
```yaml
datasources:
  datasources.yaml:
    apiVersion: 1
    datasources:
      - name: Prometheus
        type: prometheus
        url: http://seldon-monitoring-prometheus.seldon-monitoring.svc.cluster.local:9090
        isDefault: true
```
Теперь можем устанавливать `Grafana`:
```shell
helm repo add grafana https://grafana.github.io/helm-charts

helm upgrade --install grafana-seldon-monitoring grafana/grafana \
             --version 6.56.1 \
             --values values_grafana_local.yaml \
             --namespace seldon-monitoring
```
В сообщении об установке обратите внимание на инструкции, как получить пароль от UI

4. Проверяем:
```shell
$ kubectl get svc -n seldon-monitoring
NAME                                   TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
alertmanager-operated                  ClusterIP   None            <none>        9093/TCP,9094/TCP,9094/UDP   47m
grafana-seldon-monitoring              ClusterIP   10.96.238.218   <none>        80/TCP                       42m
prometheus-operated                    ClusterIP   None            <none>        9090/TCP                     47m
seldon-monitoring-alertmanager         ClusterIP   10.96.47.142    <none>        9093/TCP                     48m
seldon-monitoring-blackbox-exporter    ClusterIP   10.96.1.107     <none>        19115/TCP                    48m
seldon-monitoring-kube-state-metrics   ClusterIP   10.96.134.113   <none>        8080/TCP                     48m
seldon-monitoring-node-exporter        ClusterIP   10.96.177.3     <none>        9100/TCP                     48m
seldon-monitoring-operator             ClusterIP   10.96.156.227   <none>        8080/TCP                     48m
seldon-monitoring-prometheus           ClusterIP   10.96.251.31    <none>        9090/TCP                     48m
```
Для доступа к `Grafana` осталось выполнить:
```shell
kubectl port-forward -n seldon-monitoring svc/grafana-seldon-monitoring 3000:80
```
5. Подготовим `PodMonitor` для мониторинга метрик из `SeldonDeployment`'ов:
<h5 a><strong><code>seldon-podmonitor.yaml</code></strong></h5>

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: seldon-podmonitor
  namespace: seldon-monitoring
spec:
  selector:
    matchLabels:
      app.kubernetes.io/managed-by: seldon-core
  podMetricsEndpoints:
    - port: metrics
      path: /prometheus
  namespaceSelector:
    any: true
```
6. И также подготовим сам `SeldonDeployment`(см. [tutorial](../sem_20240319/tutorial.md))

### Grafana
1. `Grafana` будет доступна по адресу `http://localhost:3000/`, какой логин и пароль использовать она вам сама рассказала во время установки с помощью `Helm`
2. Проверим, что `Grafana` связалась с `Prometheus` для получения данных: для этого перейдем во вкладку `Explore` и там в наших источниках уже будет виден `Prometheus`. Можем выполнить в нем, например, такой запрос:
```sql
model_infer_request_success_total
```
и сразу же применить необходимые фильтры по лейблам. Увидим картинку, аналогичную тому, что видели в UI `Prometheus` (если, конечно, мы не забыли предварительно отправить infer requests нашему `SeldonDeployment`).

3. Теперь перейдем во вкладку `Dashboards` и ппробуем провернуть все то же самое на новом дэшборде (и посмотрим, что можно с ним еще интересного сделать в настройках дэшборда). Нажмем на `Apply`, потом на `⋮` в верхнем правом углу созданного дэшборда, и там выполним `Inspect -> PanelJSON`. Видим, что все, что мы только что сделали, можно также описать с помощью `json`'а.