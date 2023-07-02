from edge_pdf import annot_export
import streamlit as st  # 导入 streamlit 库，用于构建 Web 应用界面
import io
import pandas as pd


def readpdf(file):
    return annot_export(file,None,False)

buffer = io.BytesIO()
file = st.file_uploader("请上传文件", type="pdf")

if file is not None:
    res_xls=readpdf(file)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        res_xls.to_excel(writer, sheet_name='Sheet1', index=False)
        # writer.close()

    download2 = st.download_button(
        label="Download data as Excel",
        data=buffer,
        file_name='注释数据.xlsx',
        mime='application/vnd.ms-excel'
    )

    # 显示结果
    st.write(res_xls)

