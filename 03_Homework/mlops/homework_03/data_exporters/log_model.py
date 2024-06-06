if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

import pickle 
import os
import mlflow 




@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here

    lr, dv = data

    os.makedirs("models", exist_ok=True)

    with open("models/vectorizer.b", "wb") as f_out:
        pickle.dump(dv, f_out)
    
    experiment_name = kwargs.get("experiment_name", "yellow_taxi_prediction")
    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment(experiment_name)
    with mlflow.start_run():
        mlflow.log_artifact("models/vectorizer.b", artifact_path="preprocessor")
        mlflow.sklearn.log_model(lr, artifact_path="models_lr")


