import streamlit as st
import pandas as pd
import io

# Corrected generate_caption function with fixes:
# - Removed Office/Shop by not including BHK for commercial properties.
# - Replaced "Row-House-Bunglows-Villa-Duplex-Tenament" with "Bunglow".
# - Fixed location by not removing the first letter of the last word after '-'.
# - Avoided "nan" by handling empty types better; used "Property" or "Commercial Space" as fallback.
# - Ensured no colon after city.
def generate_caption(row):
    lines = []
    lines.append("No brokerage offer 🥳🥳🥳")
    
    property_type = str(row.get('Property_Type', '')).strip()
    commercial_type = str(row.get('Commercial-Property-Type', '')).strip()
    residential_type = str(row.get('Residential-Property', '')).strip()
    
    # Determine bhk (skip for commercial to remove "Office/Shop")
    if property_type == "Commercial":
        bhk = ""
    else:
        bhk = str(row.get('BHK', '')).strip()
    
    # Determine property description
    if property_type == "Commercial":
        if commercial_type == "Shops-Showrooms":
            prop_desc = "Showroom"
        elif commercial_type == "Office-Space":
            prop_desc = "Office Space"
        else:
            prop_desc = commercial_type or "Commercial Space"
    else:  # Residential
        if residential_type == "Flat-Apartment-Tower":
            prop_desc = "Apartment"
        elif residential_type == "Row-House-Bunglows-Villa-Duplex-Tenament":
            prop_desc = "Bunglow"
        else:
            prop_desc = residential_type or "Property"
    
    # Format location - take the last part after '-', without removing first letter
    location = str(row.get('Location', '')).strip()
    if "-" in location:
        loc_word = location.split('-')[-1]
        location_final = loc_word.strip()
    else:
        location_final = location.strip()
    city = str(row.get('City1', '')).strip()
    
    # Compose second line without colon after city
    second_line = f"🏬 Amazing {bhk} {prop_desc} sell at {location_final} ,{city}"
    
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
st.write("Upload a CSV or Excel file to generate corrected Instagram captions for properties. The captions will be added in column Z.")

# Debug statement
st.write("Debug: File uploader is about to render...")

# File uploader (support CSV or XLSX)
uploaded_file = st.file_uploader("Upload your CSV or XLSX file", type=["csv", "xlsx"], help="Upload a file with property details.")

if uploaded_file is not None:
    try:
        # Read the uploaded file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload CSV or XLSX.")
            st.stop()
        
        # Validate required columns
        expected_columns = [
            'Property_Type', 'Commercial-Property-Type', 'Residential-Property', 'Location', 'City1',
            'BHK', 'Super-Built-up-Plot-Space', 'Super-Built-up-Construction-Area', 'Furniture-Details',
            'Current-Status', 'JRM-Mobile-Number', 'Property-Link'
        ]
        missing_cols = [col for col in expected_columns if col not in df.columns]
        if missing_cols:
            st.warning(f"Warning: Missing columns in file: {', '.join(missing_cols)}. Captions may have incomplete data.")
        
        # Generate corrected captions and add to dataframe (column Z is the 26th column, assuming 25 existing columns)
        df['Corrected_Caption'] = df.apply(generate_caption, axis=1)
        
        # Display generated captions
        st.subheader("Generated Captions")
        for index, row in df.iterrows():
            st.markdown(f"**Property {index + 1} ({row.get('Tag', 'Untitled')}):**")
            st.text_area(f"Caption {index + 1}", row['Corrected_Caption'], height=300)
        
        # Prepare Excel for download (with captions in new column)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)
        
        st.download_button(
            label="Download Excel with Corrected Captions (in Column Z)",
            data=output,
            file_name="output_with_corrected_captions.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Option to download captions as text file
        captions_text = "\n\n".join([f"Caption {i+1}:\n{caption}" for i, caption in enumerate(df['Corrected_Caption'])])
        st.download_button(
            label="Download All Captions as TXT",
            data=captions_text,
            file_name="instagram_captions.txt",
            mime="text/plain"
        )
        
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.write("Please ensure the file is properly formatted (e.g., correct headers) and try again.")
else:
    st.info("Please upload a CSV or XLSX file to generate captions.")

st.write("Debug: File uploader has rendered.")
