import numpy as np
import altair as alt
import pandas as pd
import streamlit as st


df = pd.DataFrame(
  np.random.randn(200, 3),
  columns=['a', 'b', 'c'])

st.write('Below is a DataFrame:', df, 'Above is a dataframe.')

c = alt.Chart(df).mark_circle().encode(
  x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
st.write(c)