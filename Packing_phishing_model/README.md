# Guide pour Exécuter le Modèle de Détection de Phishing


## Étapes pour Exécuter le Modèle

### Installer les requirements

```bash
pip install -r Packing_phishing_model/requirements.txt
```

### Entrainer le model
```bash
python Packing_phishing_model/prediction_model/training_pipeline.py
```

### Test de l'application streamlit
```bash
streamlit run app.py
```
---

# Explication du Notebook

### Choix de la donnée caractéristiques numériques

1) Graphiques et Plots : Les caractéristiques numériques peuvent être facilement visualisées avec des graphiques tels que des histogrammes, des scatter plots  etc., facilitant ainsi l'analyse exploratoire des données.
2) Recall plus élevé lors du premier test : Dans le cadre de notre modèle de détection de phishing, j'ai choisi de surveiller principalement le Recall (ou rappel) comme métrique de performance clé car il est plus dangereux pour un utilisateur que le model prédise qu'un email est légitime alors qu'il est du fishing. Le Recall mesure la capacité du modèle à identifier correctement toutes les instances positives (c'est-à-dire les URL de phishing). Ainsi j'ai pu constater que le recall etait plus éléver en utilisant les caratecristiques numériques que les données textuelles ce qui m'a conforté dans mon choix.


### Amélioration à venir

Plus de features engineering en testant le contenu des pages web des url, vérifier s'il y a une redirection ou si des liens pointes vers l'url, l'age du domain, s'il y a des stats sur les pages web etc ...

Déploiment du code et mise en place d'un process de CI/CD utilisant Github/Github Action ou Jenkins/Dockerfile/Docker registry 

---

# Maintenance et Mise à Jour du Modèle

## Introduction
Cette documentation décrit mon approche de maintenance et de mise à jour d'un modèle de machine learning pour la détection d'URL de phishing. Elle inclut l'utilisation de Grafana pour la surveillance, une stratégie de détection de drift.

## Surveillance avec Grafana

### Configuration de Grafana

1. **Installation de Grafana** : Suivre les instructions officielles pour installer Grafana sur votre système ou utilisez une instance hébergée.
2. **Configuration de la Source de Données** :
    - Utiliser Prometheus comme source de données pour Grafana. Installez et configurez Prometheus pour collecter les métriques de votre modèle.
    - Ajouter Prometheus comme source de données dans Grafana via l'interface d'administration.

### Collecte des Métriques
1. **Exposer les Métriques du Modèle** : Utiliser une bibliothèque comme `prometheus_client` en Python pour exposer les métriques de votre modèle.
    ```python
    from prometheus_client import start_http_server, Summary

    # Créer un résumé pour suivre la latence des prédictions
    PREDICTION_LATENCY = Summary('prediction_latency_seconds', 'Time spent processing prediction')

    @PREDICTION_LATENCY.time()
    def predict():
        # Logique de prédiction du modèle
        pass

    if __name__ == '__main__':
        start_http_server(8000)  # Expose les métriques sur le port 8000
        while True:
            predict()
    ```

2. **Tableaux de Bord Grafana** : Créer des tableaux de bord Grafana pour surveiller les métriques clés telles que :
    - Précision, rappel, F1-score
    - Latence des prédictions
    - Distribution des features
    - Fréquence des alertes de drift

## Stratégie de Détection de Drift

### Détection du Drift avec le Test de Kolmogorov-Smirnov

1. **Test de Kolmogorov-Smirnov** : Utiliser le test de Kolmogorov-Smirnov pour détecter les changements dans la distribution des features.
    ```python
    import numpy as np
    from scipy.stats import ks_2samp

    def detect_drift(feature_current, feature_historical, alpha=0.05):
        """Détecter la dérive de la distribution d'une feature avec le test de Kolmogorov-Smirnov."""
        stat, p_value = ks_2samp(feature_current, feature_historical)
        drift_detected = p_value < alpha
        return drift_detected, p_value

    # Exemple d'utilisation
    historical_data = np.random.normal(0, 1, 1000)
    current_data = np.random.normal(0, 1.5, 1000)

    drift_detected, p_value = detect_drift(current_data, historical_data)
    print(f"Drift Detected: {drift_detected}, p-value: {p_value}")
    ```

2. **Alertes Automatiques** : Configurer Prometheus pour envoyer des alertes à Grafana lorsque le drift est détecté.

## Incorporation de Nouvelles Informations
Le model est sous la forme de package ce qui facile l'incorporation de nouvelles informations ainsi que de features engineering.
```bash
.
├── MANIFEST.in
├── README.md
├── prediction_model
│   ├── VERSION
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-39.pyc
│   │   ├── model.cpython-39.pyc
│   │   ├── pipeline.cpython-39.pyc
│   │   └── predict.cpython-39.pyc
│   ├── config
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-39.pyc
│   │   │   └── config.cpython-39.pyc
│   │   └── config.py
│   ├── datasets
│   │   ├── __init__.py
│   │   └── dataset.csv
│   ├── model.py
│   ├── pipeline.py
│   ├── predict.py
│   ├── processing
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-39.pyc
│   │   │   ├── data_handling.cpython-39.pyc
│   │   │   └── preprocessing.cpython-39.pyc
│   │   ├── data_handling.py
│   │   └── preprocessing.py
│   ├── testdata
│   │   ├── __init__.py
│   │   └── test.csv
│   ├── trained_models
│   │   └── __init__.py
│   └── training_pipeline.py
├── requirement.txt
└── setup.py
```
Pour cela il suffit de modifier le fichier de preprocessing.py
### Réentraînement Régulier
- Programmez des réentraînements réguliers du modèle avec des données récentes. Utilisez des tâches cron ou un orchestrateur de workflows comme Airflow.
    ```python
    import schedule
    import time

    def retrain_model():
        # Logique de réentraînement du modèle
        pass

    schedule.every().month.do(retrain_model)

    while True:
        schedule.run_pending()
        time.sleep(1)
    ```


## Conclusion

En suivant cette approche, vous pouvez assurer la maintenance continue et la mise à jour de votre modèle de détection d'URL de phishing. La surveillance avec Grafana, la détection de drift et l'incorporation de nouvelles informations garantiront que votre modèle reste performant et pertinent au fil du temps.

---

## Sources

https://grafana.com/blog/2021/08/02/how-basisai-uses-grafana-and-prometheus-to-monitor-model-drift-in-machine-learning-workloads/

https://enix.io/en/blog/create-prometheus-exporter/

https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ks_2samp.html
