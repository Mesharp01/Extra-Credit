import pandas as pd
import streamlit as st
from io import StringIO
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

def _max_width_():
    max_width_str = f"max-width: 1800px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )
st.title("Books Database")

c29, c30, c31 = st.columns([1, 6, 1])

with c30:
    uploaded_file = st.selectbox("Pick one", ["Accounts.csv", "Authors.csv", "CustReviews.csv", "Order_Items.csv", "Orders.csv", "Payments.csv", "Publishers.csv" ])

    if uploaded_file is not None:
        shows = pd.read_csv(uploaded_file)
        shows.drop(shows.columns[shows.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)

    else:
        st.info(
            f"""
                Select a .csv file first.
                """
        )

        st.stop()

from st_aggrid import GridUpdateMode, DataReturnMode

gb = GridOptionsBuilder.from_dataframe(shows)
gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
gb.configure_selection(selection_mode="multiple", use_checkbox=True)
gb.configure_side_bar()
gridOptions = gb.build()

st.success(
    f"""
        Hold the shift key when selecting rows to select multiple rows at once
        """
)

response = AgGrid(
    shows,
    gridOptions=gridOptions,
    enable_enterprise_modules=True,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    fit_columns_on_grid_load=False,
)

df = pd.DataFrame(response["selected_rows"])

st.subheader("Filtered data will appear below")
st.text("")

st.table(df)

st.text("")

c29, c30, c31 = st.columns([1, 1, 2])

with c29:

    @st.experimental_memo
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(df)
    st.download_button(
        "Press to Download",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv'
)
