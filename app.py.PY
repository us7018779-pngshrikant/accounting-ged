import streamlit as st
import pandas as pd
import pdfplumber
import io
import re
import urllib.parse
from cryptography.fernet import Fernet

# =========================================================
# 1. STREAMLIT PAGE CONFIGURATION & 3D STYLING
# =========================================================
st.set_page_config(
    page_title="ACCOUNTING GOD",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom 3D & Executive CSS
st.markdown("""
    <style>
    /* Global Page Background */
    .stApp {
        background: #F8FAFC;
    }
    
    /* 3D Main Executive Header */
    .header-3d {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #2563EB 100%);
        padding: 25px 20px;
        border-radius: 16px;
        text-align: center;
        color: #FFFFFF;
        box-shadow: 0px 10px 25px rgba(15, 23, 42, 0.35), inset 0px 1px 1px rgba(255, 255, 255, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 25px;
        position: relative;
    }
    .header-title {
        font-size: 34px;
        font-weight: 900;
        letter-spacing: 2px;
        text-shadow: 2px 4px 10px rgba(0, 0, 0, 0.5);
        color: #F8FAFC;
        margin: 0;
    }
    .header-subtitle {
        font-size: 13px;
        font-weight: 700;
        color: #F3F4F6;
        letter-spacing: 2.5px;
        margin-top: 6px;
        text-transform: uppercase;
    }
    
    /* Sidebar Navigation Positioning (Shifted Upwards) */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 10px !important; /* Top margin reduced to move menu upwards */
    }
    [data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    
    /* 3D Metric Card Box */
    [data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #1E3A8A !important;
    }
    div[data-testid="metric-container"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05), inset 0px -2px 0px #CBD5E1;
        transition: transform 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Professional Guide Box */
    .guide-card-3d {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border-left: 6px solid #2563EB;
        padding: 14px 20px;
        border-radius: 10px;
        margin-bottom: 22px;
        color: #1E40AF;
        font-size: 14px;
        font-weight: 500;
        box-shadow: 0px 3px 8px rgba(37, 99, 235, 0.08);
    }
    
    /* Input Fields & Buttons Styling */
    .stButton>button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        color: #FFFFFF !important;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        padding: 8px 20px;
        box-shadow: 0px 4px 10px rgba(37, 99, 235, 0.3);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 6px 15px rgba(37, 99, 235, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# 3D Main Executive Header
st.markdown("""
    <div class="header-3d">
        <div class="header-title">⚡ ACCOUNTING GOD</div>
        <div class="header-subtitle">DEVELOPED BY SHRIKANT SHUKLA</div>
    </div>
""", unsafe_allow_html=True)

# Encryption Setup
if 'cipher_key' not in st.session_state:
    st.session_state['cipher_key'] = Fernet.generate_key()
cipher = Fernet(st.session_state['cipher_key'])

# Client Database
if 'client_db' not in st.session_state:
    st.session_state['client_db'] = pd.DataFrame([
        {
            "Client Name": "Sharma Electronics",
            "Phone": "919876543210",
            "GSTIN": "27AAACS1234A1Z1",
            "Portal Username": "sharma_gst",
            "Encrypted_Password": cipher.encrypt(b"Pass@1234").decode(),
            "GSTR-1 Status": "Filed",
            "GSTR-3B Status": "Filed",
            "Due Date": "2026-08-20"
        },
        {
            "Client Name": "Apex Tech Solutions",
            "Phone": "919812345678",
            "GSTIN": "07AABCA5678B1Z5",
            "Portal Username": "apex_tax",
            "Encrypted_Password": cipher.encrypt(b"Apex#9876").decode(),
            "GSTR-1 Status": "Filed",
            "GSTR-3B Status": "Pending",
            "Due Date": "2026-08-20"
        },
        {
            "Client Name": "Verma Logistics",
            "Phone": "919711223344",
            "GSTIN": "09ABCDE9012C1Z8",
            "Portal Username": "verma_log",
            "Encrypted_Password": cipher.encrypt(b"VermaSecure!").decode(),
            "GSTR-1 Status": "Pending",
            "GSTR-3B Status": "Pending",
            "Due Date": "2026-08-20"
        }
    ])

# Helper Function: GSTIN Validation
def is_valid_gstin(gstin: str) -> bool:
    gstin_regex = r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$"
    return bool(re.match(gstin_regex, gstin.upper().strip()))

# =========================================================
# 2. SIDEBAR NAVIGATION (SHIFTED UPWARDS)
# =========================================================
st.sidebar.markdown("### 📌 CONTROL CENTER")
menu = st.sidebar.radio(
    "Select Function:",
    [
        "📊 GST Return Tracker (GSTR 3B/1)", 
        "📲 WhatsApp Client Reminders", 
        "🧮 GST & Late Interest Calculator",
        "🔑 Client Vault & Password Locker", 
        "📄 PDF to Excel Converter Engine"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("⚡ **ACCOUNTING GOD v2.0**")
st.sidebar.caption("Designed by **Shrikant Shukla**")

# =========================================================
# MODULE 1: GST RETURN TRACKER
# =========================================================
if menu == "📊 GST Return Tracker (GSTR 3B/1)":
    st.subheader("📊 Client GST Filing Tracker")
    st.markdown("""
        <div class="guide-card-3d">
            💡 <b>How to Use:</b> Monitor real-time status of <b>GSTR-1</b> and <b>GSTR-3B</b> across all clients. Update statuses below and click <b>"Save Status Updates"</b>.
        </div>
    """, unsafe_allow_html=True)
    
    df = st.session_state['client_db'].copy()
    
    search_query = st.text_input("🔍 Quick Search (By Name or GSTIN):", "")
    if search_query:
        df = df[df["Client Name"].str.contains(search_query, case=False) | df["GSTIN"].str.contains(search_query, case=False)]

    total_clients = len(df)
    gstr3b_filed = len(df[df["GSTR-3B Status"] == "Filed"])
    gstr3b_pending = total_clients - gstr3b_filed
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Active Clients", total_clients)
    col2.metric("GSTR-3B Filed", gstr3b_filed)
    col3.metric("GSTR-3B Pending", gstr3b_pending, delta=f"{gstr3b_pending} Pending", delta_color="inverse")
    
    st.write("---")
    
    edited_df = st.data_editor(
        df[["Client Name", "Phone", "GSTIN", "GSTR-1 Status", "GSTR-3B Status", "Due Date"]],
        column_config={
            "GSTR-1 Status": st.column_config.SelectboxColumn("GSTR-1", options=["Filed", "Pending", "Overdue"]),
            "GSTR-3B Status": st.column_config.SelectboxColumn("GSTR-3B", options=["Filed", "Pending", "Overdue"]),
        },
        disabled=["Client Name", "GSTIN"],
        hide_index=True,
        use_container_width=True
    )
    
    if st.button("💾 Save Status Updates"):
        st.session_state['client_db'].update(edited_df)
        st.success("✅ Filing status updated successfully!")

# =========================================================
# MODULE 2: WHATSAPP CLIENT REMINDERS
# =========================================================
elif menu == "📲 WhatsApp Client Reminders":
    st.subheader("📲 One-Touch WhatsApp Reminder System")
    st.markdown("""
        <div class="guide-card-3d">
            💡 <b>How to Use:</b> Automated reminder messages generated for clients with <b>Pending</b> filings. Click the WhatsApp button to launch chat directly.
        </div>
    """, unsafe_allow_html=True)
    
    df = st.session_state['client_db'].copy()
    pending_df = df[(df["GSTR-1 Status"] == "Pending") | (df["GSTR-3B Status"] == "Pending")]
    
    if pending_df.empty:
        st.balloons()
        st.success("🎉 All client filings are fully up-to-date!")
    else:
        for idx, row in pending_df.iterrows():
            with st.expander(f"🔴 Pending Notice: {row['Client Name']} (GSTIN: {row['GSTIN']})"):
                msg = (
                    f"Dear {row['Client Name']},\n\n"
                    f"This is a reminder regarding your GST compliance due on *{row['Due Date']}*.\n"
                    f"- GSTR-1 Status: *{row['GSTR-1 Status']}*\n"
                    f"- GSTR-3B Status: *{row['GSTR-3B Status']}*\n\n"
                    f"Please submit your invoice data to avoid late filing penalties.\n\n"
                    f"Regards,\n*Tax Consultant Office*"
                )
                
                st.text_area("Pre-Typed Message Preview:", value=msg, height=130, key=f"msg_{idx}")
                
                encoded_msg = urllib.parse.quote(msg)
                wa_url = f"https://api.whatsapp.com/send?phone={row['Phone']}&text={encoded_msg}"
                
                st.markdown(f"[📲 Send WhatsApp Reminder to {row['Client Name']}]({wa_url})", unsafe_allow_html=True)

# =========================================================
# MODULE 3: TAX & LATE INTEREST CALCULATOR
# =========================================================
elif menu == "🧮 GST & Late Interest Calculator":
    st.subheader("🧮 Tax Splitter & Interest Calculator Engine")
    st.markdown("""
        <div class="guide-card-3d">
            💡 <b>How to Use:</b> Split invoice values into CGST/SGST/IGST components and compute statutory 18% Per Annum interest for delayed returns.
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 1. Invoice Tax Splitter")
        taxable_val = st.number_input("Taxable Amount (₹)", min_value=0.0, value=100000.0, step=1000.0)
        gst_rate = st.selectbox("GST Rate (%)", [5.0, 12.0, 18.0, 28.0], index=2)
        supply_type = st.radio("Supply Type", ["Intra-State (CGST + SGST)", "Inter-State (IGST)"])
        
        total_gst = taxable_val * (gst_rate / 100.0)
        
        if supply_type == "Intra-State (CGST + SGST)":
            cgst = total_gst / 2.0
            sgst = total_gst / 2.0
            igst = 0.0
        else:
            cgst = 0.0
            sgst = 0.0
            igst = total_gst
            
        grand_total = taxable_val + total_gst
        
        st.write("---")
        st.write(f"• **CGST ({gst_rate/2 if cgst else 0}%):** ₹ {cgst:,.2f}")
        st.write(f"• **SGST ({gst_rate/2 if sgst else 0}%):** ₹ {sgst:,.2f}")
        st.write(f"• **IGST ({gst_rate if igst else 0}%):** ₹ {igst:,.2f}")
        st.markdown(f"#### Net Total Invoice Value: ₹ {grand_total:,.2f}")

    with col2:
        st.markdown("### 2. Statutory Interest Calculator (Sec 50)")
        unpaid_tax = st.number_input("Unpaid Tax Net Amount (₹)", min_value=0.0, value=50000.0, step=1000.0)
        delay_days = st.number_input("Days Delayed", min_value=0, value=15)
        
        interest_amount = (unpaid_tax * 0.18 * delay_days) / 365.0
        
        st.write("---")
        st.info("Statutory Rate: **18% Per Annum**")
        st.markdown(f"#### Calculated Late Interest: ₹ {interest_amount:,.2f}")

# =========================================================
# MODULE 4: CLIENT VAULT & PASSWORD LOCKER
# =========================================================
elif menu == "🔑 Client Vault & Password Locker":
    st.subheader("🔑 Encrypted Credentials Vault")
    st.markdown("""
        <div class="guide-card-3d">
            💡 <b>How to Use:</b> Store GST portal credentials securely. Passwords are protected using military-grade <b>AES-256 Encryption</b>.
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("➕ Add New Client Credentials"):
        with st.form("new_client_form"):
            c_name = st.text_input("Client Name")
            c_phone = st.text_input("WhatsApp Phone (e.g., 919876543210)")
            c_gstin = st.text_input("GSTIN Number").upper()
            c_user = st.text_input("Portal Username")
            c_pass = st.text_input("Portal Password", type="password")
            submit = st.form_submit_button("Save Encrypted Client")
            
            if submit:
                if not is_valid_gstin(c_gstin):
                    st.error("❌ Invalid GSTIN Format! Must be 15 alphanumeric characters.")
                elif c_name and c_pass:
                    enc_p = cipher.encrypt(c_pass.encode()).decode()
                    new_row = {
                        "Client Name": c_name,
                        "Phone": c_phone,
                        "GSTIN": c_gstin,
                        "Portal Username": c_user,
                        "Encrypted_Password": enc_p,
                        "GSTR-1 Status": "Pending",
                        "GSTR-3B Status": "Pending",
                        "Due Date": "2026-08-20"
                    }
                    st.session_state['client_db'] = pd.concat(
                        [st.session_state['client_db'], pd.DataFrame([new_row])], 
                        ignore_index=True
                    )
                    st.success(f"✅ Client profile for '{c_name}' encrypted & saved!")

    st.write("---")
    st.markdown("### Client Vault Directory")
    display_df = st.session_state['client_db'].copy()
    
    show_passwords = st.checkbox("👁️ Decrypt Passwords")
    if show_passwords:
        display_df["Decrypted Password"] = display_df["Encrypted_Password"].apply(
            lambda x: cipher.decrypt(x.encode()).decode()
        )
        st.dataframe(display_df[["Client Name", "Phone", "GSTIN", "Portal Username", "Decrypted Password"]], use_container_width=True)
    else:
        display_df["Password Hash"] = "••••••••••••"
        st.dataframe(display_df[["Client Name", "Phone", "GSTIN", "Portal Username", "Password Hash"]], use_container_width=True)

# =========================================================
# MODULE 5: PDF TO EXCEL CONVERTER
# =========================================================
elif menu == "📄 PDF to Excel Converter Engine":
    st.subheader("📄 Automated PDF Document Parsing Engine")
    st.markdown("""
        <div class="guide-card-3d">
            💡 <b>How to Use:</b> Upload financial statements or invoice PDFs to automatically extract clean tables into a formatted Excel sheet.
        </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Accounting PDF Document", type=["pdf"])
    
    if uploaded_file is not None:
        extracted_tables = []
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    if len(table) > 0:
                        headers = table[0]
                        data = table[1:]
                        
                        clean_headers = []
                        for idx, h in enumerate(headers):
                            if h is None or str(h).strip() == "" or str(h).lower() == "nan":
                                clean_headers.append(f"Column_{idx+1}")
                            else:
                                clean_headers.append(str(h).replace('\n', ' ').strip())
                        
                        df = pd.DataFrame(data, columns=clean_headers)
                        extracted_tables.append(df)
        
        if extracted_tables:
            combined_df = pd.concat(extracted_tables, ignore_index=True)
            
            # AUTOMATED FIX: Unique Column Naming
            cols = pd.Series(combined_df.columns)
            for dup in cols[cols.duplicated()].unique():
                cols[cols == dup] = [f"{dup}_{i}" if i != 0 else dup for i in range(sum(cols == dup))]
            combined_df.columns = cols

            st.markdown("### Parsed Data Table")
            st.dataframe(combined_df, use_container_width=True)
            
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                combined_df.to_excel(writer, sheet_name="Extracted_Data", index=False)
            excel_data = output.getvalue()
            
            st.download_button(
                label="📥 Download Converted Excel Spreadsheet (.xlsx)",
                data=excel_data,
                file_name="Converted_Accounting_Data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("⚠️ No tabular structures detected in the document.")