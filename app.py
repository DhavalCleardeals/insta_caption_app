import streamlit as st
import pandas as pd
import io

# Corrected generate_caption function
def generate_caption(row):
    lines = []
    lines.append("No brokerage offer 🥳🥳🥳")

    # Clean data from row
    property_type = str(row.get('Property_Type', '')).strip()
    commercial_type = str(row.get('Commercial-Property-Type', '')).strip()
    residential_type = str(row.get('Residential-Property', '')).strip()
    bhk = str(row.get('BHK', '')).strip()

    # Determine property description
    if property_type == "Commercial":
        bhk = "" # Skip BHK for commercial
        if commercial_type == "Shops-Showrooms":
            prop_desc = "Showroom"
        elif commercial_type == "Office-Space":
            prop_desc = "Office Space"
        elif commercial_type in ["nan", ""]:
            prop_desc = "Commercial Space"
        else:
            prop_desc = commercial_type
    else:  # Residential logic
        if residential_type == "Flat-Apartment-Tower":
            prop_desc = "Apartment"
        elif residential_type == "Row-House-Bunglows-Villa-Duplex-Tenament":
            prop_desc = "Bunglow"
        elif residential_type in ["nan", ""]:
            prop_desc = "Property"
        else:
            prop_desc = residential_type

    # Format location
    location = str(row.get('Location', '')).strip()
    if "-" in location:
        loc_word = location.split('-')[-1].strip()
        # Remove only leading letter of loc_word if needed
        location_final = loc_word[1:] if len(loc_word) > 1 else loc_word
    else:
        location_final = location

    city = str(row.get('City1', '')).strip()

    # Compose second line
    bhk_prefix = f"{bhk} " if bhk else ""
    second_line = f"🏬 Amazing {bhk_prefix}{prop_desc} for sale at {location_final}, {city}"
    lines.append(second_line)
    lines.append("")  # blank line

    # Details Section
    lines.append(f"✨ Area: {row.get('Super-Built-up-Plot-Space', '')} / {row.get('Super-Built-up-Construction-Area', '')}")
    lines.append(f"🛋️ Furniture: {row.get('Furniture-Details', '')}")
    lines.append(f"📌 Status: {row.get('Current-Status', '')}")
    lines.append("")
    lines.append("🤝 Contact for visit:")
    lines.append(f"📞 {row.get('JRM-Mobile-Number', '')}")
    lines.append("📞 8401647877")
    lines.append("📞 9104452244") 
    lines.append("(Time: 11 am to 6 pm)")
    lines.append("")
    lines.append("To Promote your Property:")
    lines.append("DM @cleardeals.pune")
    lines.append("")
    lines.append(f"For more details visit: {row.get('Property-Link','')}")
    lines.append("#propertytour #cleardeals #ahmedabadrealestate #punerealestate #trending #viralreels")
    
    return "\n".join(lines)

# --- Streamlit UI ---
st.set_page_config(page_title="Instagram Caption Generator", layout="wide")
st.title("Instagram Caption Generator")

uploaded_file = st.file_uploader("Upload your CSV or XLSX file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Apply caption generation
        df['Corrected_Caption'] = df.apply(generate_caption, axis=1)
        
        st.subheader("Generated Captions Preview")
        st.dataframe(df[['Corrected_Caption']].head())
        
        # Download Buttons
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        
        st.download_button(
            label="Download Excel with Captions",
            data=output.getvalue(),
            file_name="property_captions.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Awaiting file upload...")