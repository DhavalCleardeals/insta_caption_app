import streamlit as st
import pandas as pd
import io

# Define the generate_caption function (unchanged from your original)
def generate_caption(row):
    lines = []
    lines.append("No brokerage offer 🥳🥳🥳")
    
    # Fix Property_Type & Commercial-Property-Type replacement for Office/Shop
    property_type = str(row.get('Property_Type', '')).strip()
    commercial_type = str(row.get('Commercial-Property-Type', '')).strip()
    residential_type = str(row.get('Residential-Property', '')).strip()
    
    # Determine property description for second line
    if property_type == "Commercial":
        # Replace "Office/Shop" with column G mapping
        if commercial_type == "Shops-Showrooms":
            prop_desc = "Showroom"
        elif commercial_type == "Office-Space":
            prop_desc = "Office Space"
        elif commercial_type == "nan" or commercial_type == "":
            prop_desc = "is available to"
        else:
            prop_desc = commercial_type or "Commercial Space"
    else:  # Residential logic
        if residential_type in ["Flat-Apartment-Tower"]:
            prop_desc = "Apartment"
        elif residential_type == "nan" or residential_type == "":
            prop_desc = "is available to"
        else:
            prop_desc = residential_type
    
    # Format location (last word after '-' but removing first letter only if it exists)
    location = str(row.get('Location', ''))
    if location and "-" in location:
        loc_word = location.split('-')[-1]
        # Remove only leading letter of loc_word
        loc_word = loc_word[1:] if len(loc_word) > 1 else loc_word
        location_final = loc_word.strip()
    else:
        location_final = location.strip()
    city = str(row.get('City1', '')).strip()
    
    # Compose second line without colon after city
    second_line = f"🏬 Amazing {row.get('BHK', '')} {prop_desc} sell at {location_final} ,{city}"
    
    lines.append(second_line)
    lines.append("")  # blank line
    
    lines.append(f"👉 Super Built up Plot Space : {row.get('Super-Built-up-Plot-Space', '')}, Super Built up Construction Area : {row.get('Super-Built-up-Construction-Area', '')}")
    lines.append(f"👉 {row.get('Furniture-Details','')}")
    lines.append(f"👉 Current Status : {row.get('Current-Status','')}")
    lines.append("")
    lines.append("🤝 Contact for visit:")
    lines.append(f"📞 {row.get('JRM-Mobile-Number', '')}")
    lines.append("📞 8401647877")
    lines.append("(Time: 11 am to 6 pm)")
    lines.append("")
    lines.append("To Promote your Property:")
    lines.append("📞8401732226")
    lines.append("If you like our property tour please follow our account")
    lines.append("@cleardeals.ahmedabad.west")
    lines.append("@cleardeals.ahmedabad.east")
    lines.append("@cleardeals.Pune")
    lines.append("@cleardeals.gandhinagar")
    lines.append(f"For more details visit: {row.get('Property-Link','')}")
    lines.append("#propertytour #cleardeals.ahmedabad.west #cleardeals.ahmedabad.east #cleardeals.Pune cleardeals.gandhinagar #trendyproperty #ahmedabadrealestate #punerealestate #trending #trendingreels #viralreels #Newproperty")
    return "\n".join(lines)

# Streamlit app
st.set_page_config(page_title="Instagram Caption Generator", layout="wide")
st.title("Instagram Caption Generator")
st.write("Upload a CSV file to generate Instagram captions for properties.")

# Debug statement to confirm code reaches this point
st.write("Debug: File uploader is about to render...")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], help="Upload a CSV with property details.")

if uploaded_file is not None:
    try:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)
        
        # Validate required columns (optional, but good for robustness)
        expected_columns = [
            'Property_Type', 'Commercial-Property-Type', 'Residential-Property', 'Location', 'City1',
            'BHK', 'Super-Built-up-Plot-Space', 'Super-Built-up-Construction-Area', 'Furniture-Details',
            'Current-Status', 'JRM-Mobile-Number', 'Property-Link'
        ]
        missing_cols = [col for col in expected_columns if col not in df.columns]
        if missing_cols:
            st.warning(f"Warning: Missing columns in CSV: {', '.join(missing_cols)}. Captions may have incomplete data.")
        
        # Generate captions for each row
        st.subheader("Generated Captions")
        for index, row in df.iterrows():
            caption = generate_caption(row)
            st.markdown(f"**Property {index + 1}:**")
            st.text_area(f"Caption {index + 1}", caption, height=300)
            
        # Option to download captions as a text file
        captions = [generate_caption(row) for _, row in df.iterrows()]
        captions_text = "\n\n".join([f"Caption {i+1}:\n{caption}" for i, caption in enumerate(captions)])
        st.download_button(
            label="Download All Captions",
            data=captions_text,
            file_name="instagram_captions.txt",
            mime="text/plain"
        )
        
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.write("Please ensure the CSV is properly formatted and try again.")
else:
    st.info("Please upload a CSV file to generate captions.")

st.write("Debug: File uploader has rendered.")
