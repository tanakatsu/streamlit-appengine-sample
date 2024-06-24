import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import streamlit as st
from gcs import GCS


GCS_OUTPUT_FILEPATH = "test.pkl"

bucket_name = os.environ["GCS_BUCKET_NAME"]
gcs = GCS(bucket_name)


def plot(fig_placeholder, data: np.ndarray):
    fig, ax = plt.subplots()
    ax.hist(data)
    fig_placeholder.pyplot(fig)


if "valid_bucket" not in st.session_state:
    st.session_state["valid_bucket"] = gcs.bucket_exists()

st.title("Gaussian distribution generation")
col_mu, col_sigma, col_n = st.columns(3)
with col_mu:
    mu = st.number_input("mu", value=0.0, step=0.1)
with col_sigma:
    sigma = st.number_input("sigma", value=1.0, step=0.1)
with col_n:
    n_points = st.number_input("N", value=100, step=100)

fig_placeholder = st.empty()

generate_btn = st.button("Generate")
action_buttons, _ = st.columns(2)
with action_buttons:
    col_save, col_load, col_clear, _ = st.columns((1, 1, 1, 1))
    with col_save:
        save_btn = st.button("Save", disabled=(not st.session_state["valid_bucket"]))
    with col_load:
        load_btn = st.button("Load", disabled=(not st.session_state["valid_bucket"]))
    with col_clear:
        clear_btn = st.button("Clear")

if clear_btn:
    if 'data' in st.session_state:
        del st.session_state['data']

if load_btn:
    if gcs.blob_exists(GCS_OUTPUT_FILEPATH):
        pkl_data = gcs.download_blob_into_memory(GCS_OUTPUT_FILEPATH)
        data = pickle.loads(pkl_data)
        st.session_state['data'] = data
        plot(fig_placeholder, data)

if save_btn:
    if 'data' in st.session_state:
        upload_data = pickle.dumps(st.session_state.data)
        gcs.upload_blob_from_file(upload_data, GCS_OUTPUT_FILEPATH)
        plot(fig_placeholder, st.session_state.data)

if generate_btn:
    data = np.random.normal(mu, sigma, n_points)
    st.session_state['data'] = data
    plot(fig_placeholder, data)
