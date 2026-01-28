import streamlit as st
import pandas as pd
from datetime import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="Vata Kitchen", layout="wide")

# --- DATABASE SETUP ---
# In a real app, this would be a SQL database, but for simplicity, we use CSVs.
if 'recipes' not in st.session_state:
    st.session_state.recipes = pd.DataFrame(columns=['Name', 'Category', 'Prep Time', 'Protein', 'Ingredients', 'Steps', 'User'])

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🌿 Vata Kitchen")
page = st.sidebar.selectbox("Go to:", ["Today's Meals", "Add a Recipe", "Recipe Vault", "Grocery List"])

# --- PAGE 1: HOME (TODAY'S MEALS) ---
if page == "Today's Meals":
    st.header(f"📅 Menu for {datetime.now().strftime('%A, %b %d')}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🍳 Breakfast")
        st.selectbox("Select Meal", st.session_state.recipes[st.session_state.recipes['Category'] == 'Breakfast']['Name'], key='b')
    with col2:
        st.subheader("☀️ Lunch")
        st.selectbox("Select Meal", st.session_state.recipes[st.session_state.recipes['Category'] == 'Lunch']['Name'], key='l')
    with col3:
        st.subheader("🌙 Dinner")
        st.selectbox("Select Meal", st.session_state.recipes[st.session_state.recipes['Category'] == 'Dinner']['Name'], key='d')

# --- PAGE 2: ADD A RECIPE ---
elif page == "Add a Recipe":
    st.header("📝 Submit New High-Protein Recipe")
    with st.form("recipe_form"):
        name = st.text_input("Recipe Name")
        cat = st.selectbox("Category", ["Breakfast", "Lunch", "Dinner", "Snack"])
        prep = st.number_input("Prep Time (mins)", min_value=0)
        prot = st.number_input("Protein per serving (g)", min_value=0)
        ing = st.text_area("Ingredients (Separate with commas)")
        steps = st.text_area("Cooking Steps")
        user = st.text_input("Submitted By")
        
        if st.form_submit_button("Save to Vault"):
            new_data = pd.DataFrame([[name, cat, prep, prot, ing, steps, user]], 
                                    columns=['Name', 'Category', 'Prep Time', 'Protein', 'Ingredients', 'Steps', 'User'])
            st.session_state.recipes = pd.concat([st.session_state.recipes, new_data], ignore_index=True)
            st.success(f"Added {name} to the vault!")

# --- PAGE 3: RECIPE VAULT ---
elif page == "Recipe Vault":
    st.header("📖 All Recipes")
    st.dataframe(st.session_state.recipes, use_container_width=True)

# --- PAGE 4: GROCERY LIST ---
elif page == "Grocery List":
    st.header("🛒 Automated Grocery List")
    selected_meals = st.multiselect("Pick meals to shop for:", st.session_state.recipes['Name'])
    
    if selected_meals:
        all_ingredients = []
        for meal in selected_meals:
            items = st.session_state.recipes[st.session_state.recipes['Name'] == meal]['Ingredients'].values[0]
            all_ingredients.extend([i.strip() for i in items.split(",")])
        
        unique_ingredients = sorted(list(set(all_ingredients)))
        for item in unique_ingredients:
            st.checkbox(item)
