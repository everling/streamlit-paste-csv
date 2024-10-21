import streamlit as st
from streamlit_paste_csv import paste_csv_button


def main():
    st.title('Paste tabular data with a button click')

    separator = st.selectbox(
        "Select the separator used in your data:",
        options=[",", "\t", ";"],
        format_func=lambda x: "Comma (,)" if x == "," else "Tab (\\t)" if x == "\t" else "Semicolon (;)"
    )

    paste_result = paste_csv_button(
        label="📋 Paste tabular data",
        separator=separator,
        background_color="#FF0000",
        hover_background_color="#380909",
        errors='raise')

    if paste_result.dataframe is not None:
        st.write('Pasted data:')
        st.dataframe(paste_result.dataframe)


if __name__ == "__main__":
    main()