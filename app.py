import streamlit as st
import pandas as pd
from datetime import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="HomiesKitchen", layout="wide", page_icon="🥘")

# --- DATA STORAGE ---
# Note: In a live session, these reset on refresh. Permanent storage (Google Sheets) is the next logical step.
if 'recipes' not in st.session_state:
    st.session_state.recipes = []
if 'comments' not in st.session_state:
    st.session_state.comments = {} # Keyed by recipe name

COMMON_INGREDIENTS = ["Tofu", "TVP", "Chickpeas", "Quinoa", "Soy Milk", "Oats", "Hemp Hearts", "Peanut Butter", "Greek Yogurt", "Sweet Potato", "Normandy Veggies"]

# --- SIDEBAR ---
st.sidebar.title("🥘 HomiesKitchen")
page = st.sidebar.selectbox("Go to:", ["Today's Menu", "Add a Recipe", "Recipe Vault"])

# --- PAGE 1: TODAY'S MENU ---
if page == "Today's Menu":
    st.header("🍴 Plan Your Meals")
    if not st.session_state.recipes:
        st.info("The vault is empty! Add a recipe first.")
    else:
        servings = st.number_input("How many people are eating?", min_value=1, value=1)
        col1, col2, col3 = st.columns(3)
        slots = [("Breakfast", col1), ("Lunch", col2), ("Dinner", col3)]
        
        for slot_name, column in slots:
            with column:
                st.subheader(f"{slot_name}")
                options = [r['name'] for r in st.session_state.recipes if r['category'] == slot_name]
                selected = st.selectbox(f"Select {slot_name}", ["None"] + options)
                if selected != "None":
                    recipe = next(r for r in st.session_state.recipes if r['name'] == selected)
                    if recipe['image']:
                        st.image(recipe['image'], use_container_width=True)
                    st.success(f"**Protein:** {recipe['protein'] * servings}g")
                    for _, row in recipe['ingredients'].iterrows():
                        st.write(f"• {row['Qty'] * servings}{row['Unit']} {row['Name']}")

# --- PAGE 2: ADD A RECIPE ---
elif page == "Add a Recipe":
    st.header("📝 Create a Base Recipe")
    with st.form("recipe_form", clear_on_submit=True):
        name = st.text_input("Recipe Name")
        cat = st.selectbox("Category", ["Breakfast", "Lunch", "Dinner"])
        col_p, col_u = st.columns(2)
        prep = col_p.number_input("Prep Time (mins)", min_value=5)
        prot = col_u.number_input("Protein per 1 Serving (g)", min_value=0)
        
        st.write("### 1. Ingredients")
        st.caption("Click 'Add Row' below to add multiple ingredients.")
        df_template = pd.DataFrame([{"Name": "Tofu", "Qty": 150.0, "Unit": "g"}])
        ing_df = st.data_editor(df_template, num_rows="dynamic")
        
        st.write("### 2. Cooking Steps")
        steps_raw = st.text_area("Enter each step on a NEW LINE", placeholder="1. Press the tofu\n2. Cube it\n3. Sauté...")
        
        st.write("### 3. Visuals & Attribution")
        img_file = st.file_uploader("Upload a photo of the dish", type=['jpg', 'png', 'jpeg'])
        user = st.text_input("Submitted By")
        
        if st.form_submit_button("Save to HomiesKitchen"):
            st.session_state.recipes.append({
                'name': name, 'category': cat, 'prep': prep, 'protein': prot,
                'ingredients': ing_df, 'steps': steps_raw.split('\n'), 
                'image': img_file, 'user': user, 'likes': 0, 'dislikes': 0
            })
            st.session_state.comments[name] = []
            st.success(f"Successfully added {name}!")

# --- PAGE 3: RECIPE VAULT (Interactive) ---
elif page == "Recipe Vault":
    st.header("📖 Your Recipe Vault")
    for i, r in enumerate(st.session_state.recipes):
        with st.expander(f"📖 {r['name']} (by {r['user']})"):
            c1, c2 = st.columns([1, 2])
            with c1:
                if r['image']:
                    st.image(r['image'], use_container_width=True)
                st.write(f"**Category:** {r['category']}")
                st.write(f"**Protein:** {r['protein']}g")
            with c2:
                st.write("**Method:**")
                for idx, step in enumerate(r['steps']):
                    if step.strip(): st.write(f"{idx+1}. {step}")
            
            # Reactions
            ra1, ra2, ra3 = st.columns([1, 1, 8])
            if ra1.button(f"👍", key=f"lk_{i}"): r['likes'] += 1
            if ra2.button(f"👎", key=f"dl_{i}"): r['dislikes'] += 1
            ra3.write(f"Score: {r['likes']} Likes | {r['dislikes']} Dislikes")
            
            # Comments
            st.write("---")
            st.subheader("Comments")
            for comment in st.session_state.comments.get(r['name'], []):
                st.write(f"**{comment['user']}**: {comment['text']}")
            
            with st.form(f"comment_{i}", clear_on_submit=True):
                c_user = st.text_input("Your Name", key=f"un_{i}")
                c_text = st.text_area("Add a comment...", key=f"ct_{i}")
                if st.form_submit_button("Post"):
                    st.session_state.comments[r['name']].append({'user': c_user, 'text': c_text})
                    st.rerun()
