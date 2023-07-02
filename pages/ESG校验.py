import pandas as pd  # 导入 pandas 库，用于数据处理
import streamlit as st  # 导入 streamlit 库，用于构建 Web 应用界面
import io


st.title('ESG数据整理')
st.header('功能')
st.text('1、请确保证字段“券内部编码”不为空,程序会过滤“券内部编码”为空的数据')
st.text('2、指标类型等于FIC000003RQA的，指标代码置为NULL')


def esg_dataOS(data: pd.DataFrame):
    """
    这个函数的功能是根据一些条件对数据进行处理和计算，并将结果保存成 Excel 文件提供下载。
    
    参数:
        - data: pd.DataFrame，待处理的数据
        
    返回:
        无返回值，直接将结果保存成 Excel 文件并提供下载
    """
    # 从数据中选择需要的列，并删除空值行
    new_df = data[["证券内部编码","信息发布日期","信息来源编码","财报截止日期","业务类型","财政年度","财报起始日期","指标原始名称","指标代码","指标值","指标单位","指标单位(原始名称)","币种","指标内容","原文","日期标志","合并标志","页码"]].dropna(subset=['证券内部编码'])
    new_df['信息发布日期'] =  pd.to_datetime(new_df['信息发布日期']).dt.date
    new_df['财报截止日期'] =  pd.to_datetime(new_df['财报截止日期']).dt.date
    new_df['财报起始日期'] =  pd.to_datetime(new_df['财报起始日期']).dt.date
    new_df['财政年度'] =  pd.to_datetime(new_df['财政年度']).dt.date
    new_df[new_df['指标代码']=="FIC000003RQA"]["指标单位"]=None
    # 将结果保存成 Excel 文件并提供下载st
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        new_df.to_excel(writer, sheet_name='Sheet1', index=False)
        # writer.close()

    download2 = st.download_button(
        label="Download data as Excel",
        data=buffer,
        file_name='ESG数据.xlsx',
        mime='application/vnd.ms-excel'
    )

    # 显示结果
    st.write(new_df)


# 将数字转换为 ASCII 码对应的字符
def convert_to_ascii(s):
    return chr(int(s + 66))


# 在 Streamlit 页面上创建上传文件的选项
buffer = io.BytesIO()
file = st.file_uploader("请上传文件", type="xlsx")

# 如果有文件被上传，则读取上传的文件并调用因子配置函数
if file is not None:
    data = pd.read_excel(file, 0, dtype=str,skiprows=1)
    esg_dataOS(data)
