"""Table of Olympic Medals."""

import streamlit as st
import pandas as pd


def calculate_weighted_total(
    data: pd.DataFrame,
    gold_weight: int = 1,
    silver_weight: int = 0,
    bronze_weight: int = 0,
):
    return (
        gold_weight * data["Gold Medal"]
        + silver_weight * data["Silver Medal"]
        + bronze_weight * data["Bronze Medal"]
    )


st.set_page_config(page_title="Medal Table Paris 2024", page_icon="🏅")
st.title("Paris Olympics 2024 Medal Table")
st.header("Using weights for alternative rankings", divider=True)

st.markdown("""
        Traditionally, the table of olympic medals prioritises the number of gold medals won.
        If countries have the same number of gold medals, the order is then dictated by
        the number of silver medals, and finally bronze if the numbers are still identical.
            
        In this interactive medal table, a different approach is used to calculate the rank of each country.  
        The idea is to give a weight to each type of medal. The weighted total of medals is then the sum of
        the number of each type of medals multiplied by their respective weight.
        
        For example, with `Gold=4, Silver=2, Bronze=1`, France moves from the fifth to the third place
        because of their large number of silver medals.
        """)


medals = pd.read_csv("data/medals_total.csv", index_col="Country")

with st.container(border=True):
    st.subheader("Select the weight of each type of medal")
    gold_weight = st.number_input("Gold", min_value=0, max_value=5, value=1)
    silver_weight = st.number_input("Silver", min_value=0, max_value=5, value=0)
    bronze_weight = st.number_input("Bronze", min_value=0, max_value=5, value=0)

medals["Weighted Total"] = calculate_weighted_total(
    medals, gold_weight, silver_weight, bronze_weight
)
medals["Rank"] = medals["Weighted Total"].rank(method="min", ascending=False)

st.subheader("Medal Table 🥇🥈🥉")
st.dataframe(
    medals.sort_values("Rank"),
    hide_index=False,
    use_container_width=True,
    height=500,
)
