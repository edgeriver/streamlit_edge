import pandas as pd
import streamlit as st
import io

def xibu_factor(data:pd.DataFrame):
    new_df = data[['expression_id', 'expression','result_id','factor_name','result_freq']]
    new_df = new_df.dropna(subset=['expression_id'])
    result = pd.merge(new_df['result_id'],
                  new_df,
                  how='cross',
                  suffixes=["_t1","_t2"],
                  copy=True)
    result['result_id_t1'] = result['result_id_t1'].astype(str)
    result=result[result.apply(lambda x: x.result_id_t1 in x.expression, axis=1)]
    result.columns =["expression_factor_id","expression_id","expression","result_id","factor_name","expression_factor_freq"]
    result["expression_id"]=result["expression_id"].astype('int')
    result["expression_factor_freq"]=result["expression_factor_freq"].astype('int')
    result["data_code"]='聚源'
    result.sort_values(by=['expression_id', 'expression_factor_id'], ascending=[True, True], inplace=True)
    result = result.reindex(columns=['data_code','expression_id', 'expression','expression_factor_freq','expression_factor_id','factor_name','result_id'])
    res_count=result.groupby('expression_id').agg(count_x=('expression_factor_id','count'),).reset_index()
    res_count1=res_count[res_count['count_x']==1]
    res_count2=res_count[res_count['count_x']>1]
    result2=result[result['expression_id'].isin(res_count1['expression_id'])]
    result3=result[result['expression_id'].isin(res_count2['expression_id'])& result.apply(lambda x: x.expression_factor_id !=x.result_id, axis=1)]

    result2["expression_index"]=0
    result2["expression_factor_name"]='B'
    result2["expression_factor_id"]=0
    result2["expression_factor_is_industry"]=0
    result3["expression_factor_is_industry"]=1
    result3['expression_index'] = result3.groupby('expression_id')['expression_factor_id'].rank(ascending=True)-1
    result3["expression_factor_name"]= result3['expression_index'].apply(convert_to_ascii)
    all_res = pd.concat([result2, result3], axis=0, ignore_index=True)
    all_res.sort_values(by=['expression_id', 'expression_factor_id'], ascending=[True, True], inplace=True)
    all_res = all_res.reindex(columns=["data_code","expression_id","expression_index","expression_factor_name","expression_factor_freq","expression_factor_id","expression_factor_is_industry","factor_name","result_id"])
    # result1=result[result['expression'].str.contains(result['result_id_t1'])].copy()
    # 显示数据
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    # Write each dataframe to a different worksheet.
        all_res.to_excel(writer, sheet_name='Sheet1', index=False)
        # Close the Pandas Excel writer and output the Excel file to the buffer
        writer.close()
        download2 = st.download_button(
            label="Download data as Excel",
            data=buffer,
            file_name='因子配置.xlsx',
            mime='application/vnd.ms-excel'
    )
    st.write(all_res)

def convert_to_ascii(s):
    return chr(int(s+66))

buffer = io.BytesIO()
# 创建文件上传控件
file = st.file_uploader("请上传文件", type="xlsx")
# 判断是否选择了文件
if file is not None:
    # 读取文件内容并转化为 DataFrame 格式
    data = pd.read_excel(file,"表达式配置",dtype=str)
    xibu_factor(data)

