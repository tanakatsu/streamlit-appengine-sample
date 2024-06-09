import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import streamlit as st
from gcs import GCS


GCS_OUTPUT_FILEPATH = "test.pkl"

bucket_name = os.environ["GCS_BUCKET_NAME"]
gcs = GCS(bucket_name)

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
        save_btn = st.button("Save")
    with col_load:
        load_btn = st.button("Load")
    with col_clear:
        clear_btn = st.button("Clear")

if clear_btn:
    del st.session_state['data']

if load_btn:
    if gcs.blob_exists(GCS_OUTPUT_FILEPATH):
        pkl_data = gcs.download_blob_into_memory(GCS_OUTPUT_FILEPATH)
        data = pickle.loads(pkl_data)
        st.session_state['data'] = data

if save_btn:
    if 'data' in st.session_state:
        data = pickle.dumps(st.session_state.data)
        gcs.upload_blob_from_file(data, GCS_OUTPUT_FILEPATH)

if generate_btn:
    fig = plt.figure()
    data = np.random.normal(mu, sigma, n_points)
    st.session_state['data'] = data
    plt.hist(data)
    fig_placeholder.pyplot(fig)
elif 'data' in st.session_state:
    fig = plt.figure()
    plt.hist(st.session_state.data)
    fig_placeholder.pyplot(fig)
