## streamlit-appengine-sample

### Prerequisites

1. Create a GCP project
1. (optional) Create a GCS bucket

### How to deploy

1. Copy `app.yaml.sample` to `app.yaml` and edit it when you want to use GCS as data caching
    ```
    env_variables:
      GCS_BUCKET_NAME: "YOUR_GCS_BUCKET_NAME"
    ```
2. Deploy
    ```
    $ gcloud app deploy
    ```
    Once you deployed your app, you can browse your app by typing next command
    ```
    $ gcloud app browse
    ```
