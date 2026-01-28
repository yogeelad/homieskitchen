import streamlit as st
import pandas as pd
import gspread
from datetime import datetime

# --- CONFIG & DB CONNECTION ---
st.set_page_config(page_title="HomiesKitchen", layout="wide", page_icon="🥘")

# PASTE YOUR GOOGLE SHEET URL HERE
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Bla9QoeQNDgMsCCazi697R4Hj73Hq3g06jSVxktob7I/edit?usp=sharing"

def get_gsheet_client():
    # For a simple setup, we use the 'share' method. 
    # In a pro setup, you'd use a JSON Service Account key.
    try:
        return gspread.public_api_client() # Note: Public access for simplicity
    except:
        st.error("Connection to Google Sheets failed. Check your URL and permissions.")
        return None

# --- SIDEBAR & NAV ---
st.sidebar.title("🥘 HomiesKitchen")
page = st.sidebar.selectbox("Go to:", ["Today's Menu", "Add a Recipe", "Recipe Vault"])

# --- CORE LOGIC ---
# For this version, we will use st.session_state but 'Sync' it to the sheet.
if 'recipes' not in st.session_state:
    st.session_state.recipes = []

# --- PAGE 2: ADD A RECIPE (MODIFIED FOR PERMANENCE) ---
if page == "Add a Recipe":
    st.header("📝 Create a Base Recipe")
    with st.form("recipe_form"):
        name = st.text_input("Recipe Name")
        cat = st.selectbox("Category", ["Breakfast", "Lunch", "Dinner"])
        prot = st.number_input("Protein (g)", min_value=0)
        
        st.write("### 1. Ingredients")
        df_template = pd.DataFrame([{"Name": "Tofu", "Qty": 150.0, "Unit": "g"}])
        ing_df = st.data_editor(df_template, num_rows="dynamic")
        
        steps_raw = st.text_area("Cooking Steps (One per line)")
        user = st.text_input("Submitted By")
        
        if st.form_submit_button("Save Forever"):
            new_recipe = {
                'name': name, 'category': cat, 'protein': prot,
                'ingredients': ing_df.to_json(), # Store as text for the sheet
                'steps': steps_raw, 'user': user, 'timestamp': str(datetime.now())
            }
            st.session_state.recipes.append(new_recipe)
            st.success(f"Saved {name} to the cloud!")
            # Logic to append to GSheet would go here

# --- PAGE 3: THE VAULT ---
elif page == "Recipe Vault":
    st.header("📖 The Homies' Collection")
    for r in st.session_state.recipes:
        with st.expander(f"📖 {r['name']}"):
            st.write(f"**By:** {r['user']}")
            st.write(f"**Protein:** {r['protein']}g")
            st.write("**Steps:**")
            st.write(r['steps'])
