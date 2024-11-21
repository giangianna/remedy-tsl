import streamlit as st
import pandas as pd
from datetime import datetime

# Get the current date and time
now = datetime.now()
# Format the date and time as a string
date_now = now.strftime("%Y-%m-%d %H_%M_%S")

class Remedy:

    def bulkbanking_delete_sender(uploaded_file):
        st.subheader("Instruction")
        st.image('./instructions/Bulk Banking - Delete Sender Name.png')

        df = pd.read_excel(uploaded_file)
        
        st.subheader("Data")
        st.write(f"**{df.shape[0]}** baris, **{df.shape[1]}** kolom")
        st.dataframe(df)

        st.subheader("Result Reformating Data")
        st.dataframe(df['Sid'])

        csv = df['Sid'].to_csv(index=False, header=None)

        # Create a download button
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"bulkprem_penghapusan_remedy_{date_now}.csv",
            mime="text/csv"
        )

    def bulkbanking_insert_sender(uploaded_file):

        st.subheader("Instruction")
        st.image('./instructions/Bulk Banking - Insert Sender Name.png')
        df = pd.read_excel(uploaded_file)
        
        st.subheader("Data")
        st.write(f"**{df.shape[0]}** baris, **{df.shape[1]}** kolom")
        st.dataframe(df)
        df['1'] = 1
        df['now'] = 'now'
        df['A'] = 'A'
        # st.text(df.columns.to_list())
        df = df.reindex(columns=['co_name', 'co_login', 'pwd', 'sid', '1', 'now', 'A', 'sender', 'dlrurl'])

        st.subheader("Result Reformating Data")
        st.write(f"**{df.shape[0]}** baris, **{df.shape[1]}** kolom")
        st.dataframe(df)

        txt = df.to_csv(index=False, header=None, sep=';')

        # Create a download button
        st.download_button(
            label="Download csv",
            data=txt,
            file_name=f"bulkprem_insert_remedy_{date_now}.csv",
            mime="text/csv"
        )

    def malena_add_user_reward():
        st.warning("""There is no Nodin, we usually add a user when there is a request for a top-up bucket 
             (Pembukaan bucket GiTA), and the username is not yet registered in the database.""")
        st.image('./instructions/Malena - Add User GiTA Reward.png')
        st.write("read sample file : **reward_tsurvey.txt**")
        st.code("""reward_tsurvey,ZDkeuk825ASJF2,http://10.59.84.27:8003/callback/reward/index.php?trxid=[dlr_trxid]&status=[dlr_status]&username=reward_tsurvey,http://10.59.84.27:8003/callback/reward/index.php?trxid=[dlr_trxid]&status=[dlr_status]&username=reward_tsurvey,Data Solutions and DFS Analytics Center of Excellence Tsel""")
    
    def malena_check_bucket_by_user():
        st.warning("""No Nodin is needed. Just Input the username in the user input field on the menu. 
               An email with a snapshot of the remaining bucket for that specific username will be sent by AO.""")
        st.image('./instructions/Malena - Check Bucket Reward by User GiTA Reward_2.png')
    
    def malena_check_bucket_reward():
        st.warning("""No Nodin is needed. Submit without inputting any values, and an email with the remaining bucket snapshot for all users will be sent by AO.""")
        st.image('./instructions/Malena - Check Bucket Reward GiTA Reward.png')
    
    def malena_check_contract():
        st.write("read sample : **CheckSpecificContractID.txt**")
        st.code("""TSEL/Q02805/Djoh/8/30/2024-reward_indomog-data100mb
TSEL/Q02805/Djoh/8/30/2024-reward_indomog-data250mb
TSEL/Q02805/Djoh/8/30/2024-reward_indomog-data750mb""")
        st.image('./instructions/Malena - Check Contract GiTA Reward.png')
    
    def malena_deduct_stock(uploaded_file):

        st.subheader("Instruction")
        st.image('./instructions/Malena - Deduct Stock.png')

        df = pd.read_excel(uploaded_file)
        
        st.subheader("Data")
        st.write(f"**{df.shape[0]}** baris, **{df.shape[1]}** kolom")
        st.dataframe(df)

        # process reformating
        df = df[["contract_id", "deduct pengurangan"]]

        st.subheader("Result Reformating Data")
        st.write(f"**{df.shape[0]}** baris, **{df.shape[1]}** kolom")
        st.dataframe(df)

        txt = df.to_csv(index=False, header=None, sep='|')

        # Create a download button
        st.download_button(
            label="Download txt",
            data=txt,
            file_name=f"gita_deduct_remedy_{date_now}.txt",
            mime="text/txt"
        )

    def malena_pembukaan_bucket(uploaded_file):

        st.subheader("Instruction")
        st.image('./instructions/Malena - Pembukaan Bucket GiTA Reward.png')

        df = pd.read_excel(uploaded_file)
        
        st.subheader("Data")
        df = df.dropna()
        df.columns = df.iloc[0].to_list()
        df = df.iloc[1:].reset_index(drop=True)

        st.write(f"**{df.shape[0]}** baris, **{df.shape[1]}** kolom")
        st.dataframe(df)

        # process reformating
        df['contract_id'] = df['no.Quotation / SOA'] + '-' + df['username'] + '-' + df['reward'].str.replace("_","")
        df['quota'] = df['amount']
        df = df[['contract_id', 'username', 'reward', 'start_date', 'expired_date', 'amount', 'quota']]

        st.subheader("Result Reformating Data")
        st.write(f"**{df.shape[0]}** baris, **{df.shape[1]}** kolom")
        st.dataframe(df)

        txt = df.to_csv(index=False, header=None, sep=',')

        # Create a download button
        st.download_button(
            label="Download CSV",
            data=txt,
            file_name=f"gita_pembukaan_remedy_{date_now}.csv",
            mime="text/csv"
        )

    def malena_perpanjangan_bucket(uploaded_file):

        st.subheader("Instruction")
        st.image('./instructions/Malena - Perpanjangan Bucket GiTA Reward.png')

        df = pd.read_excel(uploaded_file)
        
        st.subheader("Data")

        condition = df.iloc[:, 0] == 'After'
        # Find the index of the row where the condition is met
        end_index = df[condition].index[0]

        # Select all rows from the start to the previous row
        before = df.iloc[:end_index]
        before = before.dropna()
        before.columns = before.iloc[0].to_list()
        before = before.iloc[1:].reset_index(drop=True)
        st.text("Before")
        st.write(f"**{before.shape[0]}** baris, **{before.shape[1]}** kolom")
        st.dataframe(before)

        # Condition to select rows where column 'A' has the value 2
        condition = df.iloc[:, 0] == 'After'

        start_index = df[condition].index[0]

        # Select the next row after the condition is met
        after = df.iloc[start_index + 1:]
        after = after.dropna().reset_index(drop=True)
        after.columns = after.iloc[0].to_list()
        after = after.iloc[1:].reset_index(drop=True)
        
        st.text("After")
        st.write(f"**{after.shape[0]}** baris, **{after.shape[1]}** kolom")
        st.dataframe(after)

        # process reformating
        after = after[['contract_id', 'expired_date']]
        after['expired_date'] = pd.to_datetime(after['expired_date']).dt.strftime("%Y-%m-%d %H:%M:%S")

        # st.write(after.dtypes)

        st.subheader("Result Reformating Data")
        st.write(f"**{after.shape[0]}** baris, **{after.shape[1]}** kolom")
        st.dataframe(after)

        txt = after.to_csv(index=False, header=None, sep=",")

        # Create a download button
        st.download_button(
            label="Download txt",
            data=txt,
            file_name=f"gita_perpanjangan_remedy_{date_now}.txt",
            mime="text/txt"
        )

    def malena_update_contract(uploaded_file):

        st.subheader("Instruction")
        st.image('./instructions/Malena - Update Contract ID, Username and Reward GiTA Reward.png')

        df = pd.read_excel(uploaded_file)
        df = df.fillna(method='ffill', axis=1)
        df = df.dropna().reset_index(drop=True)

        condition_start = df.iloc[:, 0].str.lower().str.contains('before')
        condition_end = df.iloc[:, 0].str.lower().str.contains('after')

        # Find the index of the row where the condition is met
        start_index = df[condition_start].index[0]
        end_index = df[condition_end].index[0]

        # Select all rows from the start to the previous row
        before = df.iloc[start_index+1:end_index]
        before = before.T.drop_duplicates()
        before = before.T
        before.columns = before.iloc[0].to_list()
        before = before.iloc[1:].reset_index(drop=True)

        st.subheader("Before")
        st.write(f"**{before.shape[0]}** baris, **{before.shape[1]}** kolom")
        st.dataframe(before)

        st.subheader("After")
        after = df.iloc[end_index+1:]
        after = after.T.drop_duplicates()
        after = after.T
        after.columns = after.iloc[0].to_list()
        after = after.iloc[1:].reset_index(drop=True)

        condition_end = after.iloc[:, 0].str.lower().str.contains('demikian|terima|kasih')
        end_index = after[condition_end].index[0]
        after = after.drop(end_index)

        st.write(f"**{after.shape[0]}** baris, **{after.shape[1]}** kolom")
        st.dataframe(after)

        st.subheader('Reformating Data')

        result = pd.DataFrame()
        result['contract_id_before'] = before['contract_id']
        result['contract_id_after'] = after['contract_id']
        result['username_after'] = after['username']
        result['reward_after'] = after['reward']

        st.write(f"**{result.shape[0]}** baris, **{result.shape[1]}** kolom")
        st.dataframe(result)

        txt = result.to_csv(index=False, header=None, sep=",")

        # Create a download button
        st.download_button(
            label="Download txt",
            data=txt,
            file_name=f"gita_update_contractid_username_reward_{date_now}.txt",
            mime="text/txt"
        )

    def malena_update_flag(uploaded_file):

        st.subheader("Instruction")
        st.image('./instructions/Malena - Update Flag Contract GiTA Reward.png')

        df = pd.read_excel(uploaded_file)
        df = df.fillna(method='ffill', axis=1)
        df = df.dropna().reset_index(drop=True)
        
        condition_start = df.iloc[:, 0].str.lower().str.contains('before')
        condition_end = df.iloc[:, 0].str.lower().str.contains('after')
        # Find the index of the row where the condition is met
        start_index = df[condition_start].index[0]
        end_index = df[condition_end].index[0]

                # Select all rows from the start to the previous row
        before = df.iloc[start_index+1:end_index]
        before = before.T.drop_duplicates()
        before = before.T
        before.columns = before.iloc[0].to_list()
        before = before.iloc[1:].reset_index(drop=True)

        st.subheader("Before")
        st.write(f"**{before.shape[0]}** baris, **{before.shape[1]}** kolom")
        st.dataframe(before)

        # "After"
        after = df.iloc[end_index+1:]
        after = after.T.drop_duplicates()
        after = after.T
        after.columns = after.iloc[0].to_list()
        after = after.iloc[1:].reset_index(drop=True)

        try:
            condition_end = after.iloc[:, 0].str.lower().str.contains('demikian|terima|kasih')
            end_index = after[condition_end].index[0]
            after = after.drop(end_index)
        except:
            st.success("Tidak ada footer yang mengandung kata demikian|terima|kasih")

        st.subheader("After")
        st.write(f"**{after.shape[0]}** baris, **{after.shape[1]}** kolom")
        st.dataframe(after)

        st.subheader('Reformating Data')

        after.columns = after.columns.str.lower()
        result = after[['contract_id', 'flag']]

        st.write(f"**{result.shape[0]}** baris, **{result.shape[1]}** kolom")
        st.dataframe(result)

        txt = result.to_csv(index=False, header=None, sep=";")

        # Create a download button
        st.download_button(
            label="Download txt",
            data=txt,
            file_name=f"gita_update_flag_contract_{date_now}.txt",
            mime="text/txt"
        )

    def wholeshale_inject(uploaded_file):
        import zipfile
        import io

        st.subheader("Instruction")
        st.image('./instructions/Wholesale Special Quota - Inject MPV.png')

        with st.spinner("In Progress..."):
            file = pd.ExcelFile(uploaded_file)
            sheet_names = file.sheet_names
            st.write("List of Sheet Name")
            st.write(sheet_names)

            for name in sheet_names:
                with pd.ExcelFile(uploaded_file) as xls:
                    df = pd.read_excel(xls, sheet_name=name)

                    df['BID'] = df['BID'].astype(str).str.zfill(8)

                    st.write(f"Sheet Name -> **{name}**, Jumlah Baris **{df.shape[0]}**")

                    df_tiket = df.iloc[:, 3] # index col 3 adalah kolom tiket
                    st.write(f"Jumlah Tiket ada : **{len(df_tiket.unique())} tiket**")


                    # Create a zip file in memory
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:

                        for i in df_tiket.unique().tolist():
                            df_x = df[df.iloc[:, 3] == i]
                            df_x = df_x.iloc[:, [2, 1]] # select index col 2 (Product ID) dan 1 (Serial Number)

                            # Function to convert DataFrame to CSV
                            @st.cache_data
                            def convert_df(df):
                                # df.to_csv(f"./output/reinject_{name}_{i}_{date_now}.txt", header=None, sep="|", index=False)
                                st.success(f"file Output : **reinject_{name}_{i}_{date_now}.txt**, jumlah Baris **{df_x.shape[0]}**")
                                return df.to_csv(header=None, sep="|", index=False).encode('utf-8')

                            # Convert DataFrame to CSV
                            csv = convert_df(df_x)
                            zip_file.writestr(f'inject_{name}_{i}_{date_now}.txt', csv)

                # Download button
                st.download_button(
                    label=f"Download Data Sheet {name} as zip",
                    data=zip_buffer.getvalue(),
                    file_name=f'inject_{name}_{date_now}.zip',
                    mime='application/zip'
                )