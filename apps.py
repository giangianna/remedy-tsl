import streamlit as st
import pandas as pd
from remedy import Remedy

st.title("Reformating Data Remedy - Telkomsel")

select_remedy = st.selectbox("Select Request Remedy", 
                                  options=["","BulkBanking - Delete Sender Name",
                                           "BulkBanking - Insert Sender Name",
                                           "Malena - Add User GiTA Reward",
                                           "Malena - Check Bucket Reward By User GiTA Reward",
                                           "Malena - Check Bucket Reward GiTA Reward",
                                           "Malena - Check Contract GiTA Reward",
                                           "Malena - Deduct Stock",
                                           "Malena - Pembukaan Bucket GiTA Reward",
                                           "Malena - Perpanjangan Bucket GiTA Reward",
                                           "Malena - Perubahan Start Date GiTA Reward",
                                           "Malena - Perubahan URL User GiTA Reward",
                                           "Malena - Update Contract ID, Username and Reward GiTA Reward",
                                           "Malena - Update Flag Contract GiTA Reward",
                                           "Malena - Update Quota Bucket GiTA Reward",
                                           "Wholesale Special Quota - Inject MPV",
                                           "Splunk"])

if select_remedy:
    st.write(f"Remedy yang di pilih : **{select_remedy}**")

if select_remedy == "BulkBanking - Delete Sender Name":

    uploaded_file = st.file_uploader("Choose an Excel file")

    if uploaded_file is not None:
        Remedy.bulkbanking_delete_sender(uploaded_file)
          
elif select_remedy == "BulkBanking - Insert Sender Name":

    uploaded_file = st.file_uploader("Choose an Excel file")

    if uploaded_file is not None:
        Remedy.bulkbanking_insert_sender(uploaded_file)

elif select_remedy == "Malena - Add User GiTA Reward":
    Remedy.malena_add_user_reward()

elif select_remedy == "Malena - Check Bucket Reward By User GiTA Reward":
    Remedy.malena_check_bucket_by_user()

elif select_remedy == "Malena - Check Bucket Reward GiTA Reward":
    Remedy.malena_check_bucket_reward()

elif select_remedy == "Malena - Check Contract GiTA Reward":
    Remedy.malena_check_contract()

elif select_remedy == "Malena - Deduct Stock":
    uploaded_file = st.file_uploader("Choose an Excel file")

    if uploaded_file is not None:
        Remedy.malena_deduct_stock(uploaded_file)

elif select_remedy == "Malena - Pembukaan Bucket GiTA Reward":
    uploaded_file = st.file_uploader("Choose an Excel file")

    if uploaded_file is not None:
        Remedy.malena_pembukaan_bucket(uploaded_file)

elif select_remedy == "Malena - Perpanjangan Bucket GiTA Reward":
    uploaded_file = st.file_uploader("Choose an Excel file")

    if uploaded_file is not None:
        Remedy.malena_perpanjangan_bucket(uploaded_file)

elif select_remedy == "Malena - Perubahan Start Date GiTA Reward":
    st.subheader("Instruction")
    st.image('./instructions/Malena - Perubahan Start Date GiTA Reward.png')

elif select_remedy == "Malena - Perubahan URL User GiTA Reward":
    st.subheader("Instruction")
    st.image('./instructions/Malena - Perubahan URL User GiTA Reward.png')

elif select_remedy == "Malena - Update Contract ID, Username and Reward GiTA Reward":

    uploaded_file = st.file_uploader("Choose an Excel file")

    if uploaded_file is not None:
        Remedy.malena_update_contract(uploaded_file)

elif select_remedy == "Malena - Update Flag Contract GiTA Reward":
    uploaded_file = st.file_uploader("Choose an Excel file")

    if uploaded_file is not None:
        Remedy.malena_update_flag(uploaded_file)

elif select_remedy == "Malena - Update Quota Bucket GiTA Reward":
    uploaded_file = st.file_uploader("Choose an Excel file")

    if uploaded_file is not None:

        st.subheader("Instruction")
        st.image('./instructions/Malena - Update Quota Bucket GiTA Reward.png')
        

        file = pd.ExcelFile(uploaded_file)
        sheet_names = file.sheet_names
        st.write("List of Sheet Name")
        # st.write(sheet_names)

        select_sheet = st.selectbox("Select Sheet Name", options=sheet_names)

        st.write(select_sheet)
        if select_sheet in ('original', 'validasi'):
            word_condition_start = 'pengurangan'
            word_condition_end = 'penambahan'
        else:
            word_condition_start = 'before'
            word_condition_end = 'after'

        df = pd.read_excel(file, sheet_name=select_sheet, header=None)
        st.dataframe(df)
        df = df.fillna(" ")

        condition_start = df.iloc[:, 0].str.lower().str.contains(word_condition_start)
        condition_end = df.iloc[:, 0].str.lower().str.contains(word_condition_end)

        # Find the index of the row where the condition is met
        start_index = df[condition_start].index[0]
        end_index = df[condition_end].index[0]

        if select_sheet in ('original', 'validasi'):
            pengurangan = df.iloc[start_index+1:end_index]
            st.subheader(word_condition_start.capitalize())

            condition_start = pengurangan.iloc[:, 0].str.lower().str.contains('before')
            condition_end = pengurangan.iloc[:, 0].str.lower().str.contains('after')

            # Find the index of the row where the condition is met
            start_index = pengurangan[condition_start].index[0]
            end_index = pengurangan[condition_end].index[0]

            st.write(start_index)
            st.write(end_index)

            before = pengurangan.iloc[start_index:end_index]
            before = before.T.drop_duplicates()
            before = before.T
            before.columns = before.iloc[0].to_list()
            before = before.iloc[1:].reset_index(drop=True)

            st.write("Before")
            st.dataframe(before)

            st.write("After")
            after = pengurangan.iloc[end_index:]
            st.write(end_index)
        else:
            # Select all rows from the start to the previous row
            before = df.iloc[start_index+1:end_index]
            before = before.T.drop_duplicates()
            before = before.T
            before.columns = before.iloc[0].to_list()
            before = before.iloc[1:].reset_index(drop=True)

            st.write(start_index)
            st.write(end_index)

            st.subheader("Before")
            st.dataframe(before)

            st.subheader("After")
            after = df.iloc[end_index+1:]
            after = after.T.drop_duplicates()
            after = after.T
            after.columns = after.iloc[0].to_list()
            after = after.iloc[1:].reset_index(drop=True)

            st.dataframe(after)

            after.columns = after.columns.str.lower()
            result = after[['contract_id', 'amount', 'quota']]

            st.subheader("Reformating Data")
            st.dataframe(result)

        txt = result.to_csv(index=False, header=None, sep=",")

        # Create a download button
        st.download_button(
            label="Download txt",
            data=txt,
            file_name=f"gita_konversi_update_amount_.txt",
            mime="text/txt"
        )

elif select_remedy == "Wholesale Special Quota - Inject MPV":
    uploaded_file = st.file_uploader("Choose an Excel file")

    if uploaded_file is not None:
        Remedy.wholeshale_inject(uploaded_file)

elif select_remedy == "Splunk":

    uploaded_file = st.file_uploader("Choose an Excel file")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df.shape)
        st.write(df)

        multi_select = st.multiselect("Select Columns", options=df.columns)
        st.text(multi_select)
        df = df[multi_select]
        st.write(df)

        select_for_group = st.multiselect("Select Columns for Group By", options=df.columns)
        if select_for_group:
            st.write(df.groupby(by=select_for_group).count())

