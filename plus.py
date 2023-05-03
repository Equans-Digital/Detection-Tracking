import streamlit as st
def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://www.equans.com/sites/g/files/tkmtob111/files/styles/coh_x_large/public/2022-05/EQUANS_DIGITAL_RGB.png?itok=9gZi5qIF);
                background-repeat: no-repeat;
                padding-top: 50px;
                background-position: 20px 20px;
                background-size : 300px;
                
            }
            [data-testid="stSidebarNav"]::before {
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
