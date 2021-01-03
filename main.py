import numpy
import pandas as pd
import requests
import streamlit as st


def pre_process(text: str) -> str:
    return text.replace(" ", "_").lower()


@st.cache
def get_entry(entry: str):
    response = requests.get(f"https://botw-compendium.herokuapp.com/api/v1/entry/{entry}")
    return response.status_code, response.json()


@st.cache
def get_category(cat: str):
    response = requests.get(f"https://botw-compendium.herokuapp.com/api/v1/category/{cat}")
    return response.status_code, response.json()


st.title("The legend of Zelda : Breath of the wild Compendium")

# ----------------------------------
st.header("Search by name or ID")

entry = st.text_input(label="Entry", value="Bokoblin")

entry_status_code, entry_content = get_entry(pre_process(entry))

if entry_status_code == 200:
    if entry_content["data"] == {}:
        st.write("No Results. Check for spelling or try another item")
    else:
        st.subheader(
            entry_content["data"]["name"] + " (id:" + str(entry_content["data"]["id"]) + ")"
        )
        st.write("**Category** : " + str(entry_content["data"]["category"]))
        st.write(entry_content["data"]["description"])
        st.write(pd.DataFrame(entry_content["data"]["drops"], columns=["Drops"]))
else:
    st.write("Error, This entry does not exists")

# ------------------------------------------
st.header("Browse by category")

cat = st.selectbox(
    "category", ["Treasure", "Monsters", "Equipment", "Materials", "Creatures"]
).lower()

cat_status_code, cat_contents = get_category(pre_process(cat))

if cat_status_code == 200:
    if cat == "creatures":
        food = pd.DataFrame(cat_contents["data"]["food"])
        cols = food.columns.tolist()
        food = food[cols[-1:] + cols[:-1]]
        non_food = pd.DataFrame(cat_contents["data"]["non-food"])
        df = food.merge(non_food, how="outer")
        df = df.replace(numpy.nan, "Not Food")
        st.write(df)
    else:
        df = pd.DataFrame(cat_contents["data"])
        cols = df.columns.tolist()
        df = df[cols[-1:] + cols[:-1]]
        st.write(df)

else:
    st.write("Error")
