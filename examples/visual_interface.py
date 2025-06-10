import streamlit as st
import pandas as pd
import os
import re

BASE_DIR = os.path.join(os.path.dirname(__file__), '..', 'promptbench', 'prompts', 'adv_prompts')

st.title('PromptBench Adversarial Prompts Viewer')

# List available md files
def list_files():
    files = [f for f in os.listdir(BASE_DIR) if f.endswith('.md') and f.lower() != 'readme.md']
    files.sort()
    return files

@st.cache_data
def load_prompts(filename):
    path = os.path.join(BASE_DIR, filename)
    pattern = re.compile(r"Acc: ([0-9.]+)%, prompt: (.*)")
    records = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            m = pattern.match(line.strip())
            if m:
                records.append({'Accuracy': float(m.group(1)), 'Prompt': m.group(2)})
    return pd.DataFrame(records)

md_files = list_files()
file_choice = st.selectbox('Select Model', md_files)

if file_choice:
    df = load_prompts(file_choice)
    if df.empty:
        st.write('No prompts found in', file_choice)
    else:
        st.write(df)
        st.bar_chart(df['Accuracy'])
