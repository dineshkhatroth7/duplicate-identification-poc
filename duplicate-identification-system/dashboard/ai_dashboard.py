import streamlit as st
import json
import pandas as pd
from kafka import KafkaConsumer

KAFKA_BROKER = "localhost:9092"
TOPIC = "candidate-topic"

st.set_page_config(page_title="AI Duplicate Detection Dashboard", layout="wide")

st.title("AI Duplicate Detection System Dashboard")

st.write("Real-time monitoring of candidate duplicate detection")

# Kafka Consumer
consumer = KafkaConsumer(
    "duplicate-result-topic",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="dashboard-group"
)

data = []

placeholder = st.empty()

for message in consumer:

    candidate = message.value
    data.append(candidate)

    df = pd.DataFrame(data)

    with placeholder.container():

        st.subheader("Incoming Candidates")

        st.dataframe(df)

        if "duplicate_score" in df.columns:

            st.subheader("Duplicate Score Distribution")

            st.bar_chart(df["duplicate_score"])

        if "status" in df.columns:

            st.subheader("Duplicate Status Count")

            status_count = df["status"].value_counts()

            st.bar_chart(status_count)

        if "ai_verification" in df.columns:

            st.subheader("AI Verification Results")

            ai_scores = []

            for item in df["ai_verification"]:
                if isinstance(item, dict):
                    ai_scores.append(item.get("ai_score", 0))

            if ai_scores:
                st.line_chart(ai_scores)