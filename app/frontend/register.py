import streamlit as st
import requests

def register_page():
    st.header("Register")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_pass")
    if st.button("Register"):
        if len(password) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            payload = {"email": email, "password": password}
            url = "http://localhost:8000/auth/register"
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                st.success("Account registered successfully!")
            else:
                st.error(f"Error: {response.text}")

def login_page():
    st.header("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        payload = {"email": email, "password": password}
        url = "http://localhost:8000/auth/login"
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            token = response.json()["access_token"]
            st.session_state.token = token
            st.session_state.page = "Dashboard"
            st.success("Login successful! Redirecting to dashboard...")
            st.rerun()
        else:
            st.error(f"Error: {response.text}")

def dashboard_page():
    st.header("Dashboard")
    month = st.number_input("Month", min_value=1, max_value=12, value=1)
    year = st.number_input("Year", min_value=2025, value=2025)
    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    # Generate Excel
    if st.button("Generate excel with employee aggregated data"):
        payload = {"month": int(month), "year": int(year)}
        url = "http://localhost:8000/management/create-aggregated-employee-data"
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            st.success("Excel successfully generated!")
        else:
            st.error("Error generating Excel: " + response.text)

    # Send Excel
    if st.button("Send Excel via Email"):
        payload = {"month": int(month), "year": int(year)}
        url = "http://localhost:8000/management/send-aggregated-employee-data"
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            st.success("Excel successfully sent!")
        else:
            st.error("Error sending Excel: " + response.text)

    st.markdown("---")
    st.subheader("PDF Actions")

    # Generate PDF for employees
    if st.button("Generate PDF for employees"):
        payload = {"month": int(month), "year": int(year)}
        url = "http://localhost:8000/management/create-pdf-for-empoloyees"
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            st.success("PDFs successfully generated!")
            results = response.json().get("results", [])
            st.write("PDF generated for:")
            for result in results:
                st.write(f"- {result['employee_email']}")
        else:
            st.error("Error generating PDFs: " + response.text)

    # Send PDF to employees
    if st.button("Send PDF to employees"):
        payload = {"month": int(month), "year": int(year)}
        url = "http://localhost:8000/management/send-pdf-to-employees"
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            st.success("PDF successfully sent!")
            results = response.json().get("results", [])
            st.write("PDFs sent status:")
            for result in results:
                if result.get("paycheck_sent"):
                    st.write(f"- {result['employee_email']}: ✅ Sent")
                else:
                    reason = result.get("reason", "Unknown reason")
                    st.write(f"- {result['employee_email']}: ❌ Not sent ({reason})")
        else:
            st.error("Error sending PDFs: " + response.text)

if "page" not in st.session_state:
    st.session_state.page = "Login"

page = st.sidebar.selectbox("Navigation", ["Register", "Login", "Dashboard"], index=["Register", "Login", "Dashboard"].index(st.session_state.page))

if page == "Register":
    register_page()
elif page == "Login":
    login_page()
elif page == "Dashboard":
    if "token" in st.session_state:
        dashboard_page()
    else:
        st.warning("You must be logged in to access the dashboard.")