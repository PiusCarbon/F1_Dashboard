import streamlit as st


st.header("About this project")

tab1, tab2, tab3 = st.tabs(["Support Me", "About this Project", "Report A Bug"])

with tab1:
    st.write("I am doing this in my free time. If you want to support me, reach out to my Patreon")
with tab2:
    st.write("Hi, my name is Pius. I am a 21 year old student from Germany. In my free time I love to watch F1 and python programming. So I thought: Why should I do not both)")
    st.write("This project started as an idea, when I first encountered the Formula One API 'FastF1'. I was immediately convinced that I need to create data visualizations")
with tab3:
    st.subheader("You Found A Bug")

    st.write("If you found a bug in the dashboard, I am very sorry for this. Please provide me with some information about the bug. I will fix it asap. Thank you:)")

    with st.form("Report a bug"):
        description = st.text_area("Please describe the bug")
        contact_mail = st.text_input("Your mail adress")
        upload = st.file_uploader("Screenshots", type=[".jpg", ".png"])
        submitted = st.form_submit_button("Submit")
        
        if submitted:
                if contact_mail == "" or "@" not in contact_mail or "." not in contact_mail:
                    st.error("Please provide a valid mail adress")
                else:
                    st.info("Thanks for reporting the bug!")
