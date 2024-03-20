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
   