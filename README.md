# energy-tariff-analysis

Looking at analysing the data from my Tesla battery and modelling energy provider tariffs.

This project relies on an Elasticsearch instance running. I am using my own [Docker based Elasticsearch project](https://github.com/hindmasj/my-elasticsearch-cluster). Begin by running this cluster.

## Load Some Data

Manually load a data extract using the Kibana Data Visualiser. 

1. From your space home page, go to "Analytics" -> "Machine Learning" -> "Visualize data from a file: Select file".
2. Click the selector and find a data file, e.g. *data.csv*.
3. Click "Import".
4. The index name should begin with "tesla-powerwall-" and include a date suffix that relates to the data in the file, either "yyyy-mm" for monthly data or "yyyy-mm-dd" for daily data.

## Using venv

The script is designed to work with a python virtual environment such as venv.

### Initiating Venv

```
python -m venv .venv
source .venv/bin/activate
pip install requests
```

### Using Venv

```
source .venv/bin/activate
./main.py
deactivate
```

