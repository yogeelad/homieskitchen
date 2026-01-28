import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="HomiesKitchen", layout="wide")

# --- DATA INITIALIZATION ---
if 'recipes' not in st.session_state:
    # We store ingredients as a list of dictionaries: [{'name': 'Tofu', 'base_qty': 150, 'unit': 'g'}]
    st.session_state.recipes = []

# Common ingredients for the dropdown
COMMON_INGREDIENTS = ["Tofu (Extra Firm)", "TVP", "Chickpeas", "Quinoa", "Soy Milk", "Oats", "Hemp Hearts", "Peanut Butter", "Greek Yogurt", "Sweet Potato", "Normandy Veggies"]

# --- SIDEBAR ---
st.sidebar.title("🌿 HomiesKitchen")
page = st.sidebar.selectbox("Go to:", ["Today's Menu", "Add a Recipe", "Recipe Vault"])

# --- PAGE 1: TODAY'S MENU (The Smart View) ---
if page == "Today's Menu":
    st.header("🍴 Plan Your Meals")
    
    if not st.session_state.recipes:
        st.info("Your vault is empty! Go to 'Add a Recipe' to get started.")
    else:
        # Global Serving Size Adjuster
        servings = st.number_input("How many people are eating today?", min_value=1, value=1, step=1)
        
        col1, col2, col3 = st.columns(3)
        slots = ["Breakfast", "Lunch", "Dinner"]
        cols = [col1, col2, col3]
        
        for i, slot in enumerate(slots):
            with cols[i]:
                st.subheader(f"🍳 {slot}")
                options = [r['name'] for r in st.session_state.recipes if r['category'] == slot]
                selected = st.selectbox(f"Select {slot}", ["None"] + options, key=slot)
                
                if selected != "None":
                    recipe = next(r for r in st.session_state.recipes if r['name'] == selected)
                    st.write(f"**Prep Time:** {recipe['prep']} mins")
                    st.write(f"**Protein (Total):** {recipe['protein'] * servings}g")
                    
                    st.write("---")
                    st.write("**Adjusted Ingredients:**")
                    for ing in recipe['ingredients']:
                        # This is the magic math line
                        adjusted_qty = ing['qty'] * servings
                        st.write(f"- {adjusted_qty}{ing['unit']} {ing['name']}")

# --- PAGE 2: ADD A RECIPE ---
elif page == "Add a Recipe":
    st.header("📝 Create a Base Recipe (for 1 Person)")
    with st.form("recipe_form"):
        name = st.text_input("Recipe Name")
        cat = st.selectbox("Category", ["Breakfast", "Lunch", "Dinner"])
        prep = st.number_input("Prep Time (mins)", min_value=5)
        prot = st.number_input("Protein per 1 Serving (g)", min_value=0)
        
        st.write("### Add Ingredients")
        selected_items = st.multiselect("Select common items:", COMMON_INGREDIENTS)
        other_items = st.text_input("Other items (comma separated)")
        
        st.info("Enter quantities for ONE serving. The app will multiply them later.")
        
        # We'll parse these into the structure when saving
        all_items = selected_items + ([i.strip() for i in other_items.split(",")] if other_items else [])
        
        steps = st.text_area("Cooking Steps")
        user = st.text_input("Submitted By")
        
        if st.form_submit_button("Save to HomiesKitchen"):
            # Simple parsing: For this demo, we'll assume the user adds units manually in a follow-up or just use 'units'
            ing_list = []
            for item in all_items:
                # We are creating a simple placeholder for Qty/Unit. 
                # In a more advanced version, we'd ask for these specifically.
                ing_list.append({'name': item, 'qty': 1, 'unit': 'serving'}) 
            
            st.session_state.recipes.append({
                'name': name, 'category': cat, 'prep': prep, 'protein': prot,
                'ingredients': ing_list, 'steps': steps, 'user': user
            })
            st.success(f"Saved {name}!")

# --- PAGE 3: VAULT ---
elif page == "Recipe Vault":
    st.header("📖 All Recipes")
    if st.session_state.recipes:
        st.write(st.session_state.recipes)
    else:
        st.write("No recipes found.")
