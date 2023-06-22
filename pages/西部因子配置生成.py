import pandas as pd  # 导入 pandas 库，用于数据处理
import streamlit as st  # 导入 streamlit 库，用于构建 Web 应用界面
import io


def xibu_factor(data: pd.DataFrame):
    """
    这个函数的功能是根据一些条件对数据进行处理和计算，并将结果保存成 Excel 文件提供下载。
    
    参数:
        - data: pd.DataFrame，待处理的数据
        
    返回:
        无返回值，直接将结果保存成 Excel 文件并提供下载
    """
    # 从数据中选择需要的列，并删除空值行
    new_df = data[['expression_id', 'expression', 'result_id', 'factor_name', 'result_freq']].dropna(subset=['expression_id'])

    # 对 new_df 进行自身的笛卡尔积操作，并筛选出符合条件的行
    result = pd.merge(new_df['result_id'],
                      new_df,
                      how='cross',
                      suffixes=["_t1", "_t2"],
                      copy=True)
    result['result_id_t1'] = result['result_id_t1'].astype(str)
    result["index_str"] = result.apply(lambda x: x.expression.find(x.result_id_t1), axis=1)
    result = result[result["index_str"] > -1]

    # 修改列名
    result.columns = ["expression_factor_id", "expression_id", "expression", "result_id", "factor_name", "expression_factor_freq", "index_str"]

    # 数据类型转换
    result["expression_id"] = result["expression_id"].astype('int')
    result["expression_factor_freq"] = result["expression_factor_freq"].astype('int')
    result["data_code"] = '聚源'

    # 根据 expression_id 分组并计算统计量
    res_count = result.groupby('expression_id').agg(count_x=('expression_factor_id', 'count')).reset_index()
    res_count1 = res_count[res_count['count_x'] == 1]
    res_count2 = res_count[res_count['count_x'] > 1]

    # 根据条件筛选出不同情况下的行，并进行相应的列赋值
    result2 = result[result['expression_id'].isin(res_count1['expression_id'])]
    result3 = result[result['expression_id'].isin(res_count2['expression_id']) & result.apply(lambda x: x.expression_factor_id != x.result_id, axis=1)]
    result2["expression_index"] = 0
    result2["expression_factor_name"] = 'B'
    result2["expression_factor_id"] = 0
    result2["expression_factor_is_industry"] = 0
    result3["expression_factor_is_industry"] = 1
    result3['expression_index'] = result3.groupby('expression_id')['index_str'].rank(ascending=True) - 1
    result3["expression_factor_name"] = result3['expression_index'].apply(convert_to_ascii)

    # 将 result2 和 result3 连接起来，并重新排序
    all_res = pd.concat([result2, result3], axis=0, ignore_index=True)
    all_res.sort_values(by=['expression_id', 'index_str'], ascending=[True, True], inplace=True)

    # 将 new_df 和 all_res 连接起来，并重新排序
    all_res = pd.merge(all_res, new_df[["factor_name", "result_id"]], how='left', left_on='expression_factor_id', right_on='result_id', suffixes=["_t1", "_t2"])
    all_res['factor_name_t2'] = all_res['factor_name_t2'].fillna('仅占位')
    all_res['result_id_t2'] = all_res['result_id_t2'].fillna(0)
    all_res = all_res.reindex(columns=["data_code", "expression_id", "expression_index", "expression_factor_name", "expression_factor_freq", "expression_factor_id", "expression_factor_is_industry", "factor_name_t2", "result_id_t2", "factor_name_t1", "result_id_t1", "index_str"])
    all_res.columns = ["data_code", "expression_id", "expression_index", "expression_factor_name", "expression_factor_freq", "expression_factor_id", "expression_factor_is_industry", "factor_name", "result_id", "factor_name_origin", "result_id_origin", "index_str"]
    all_res.drop("result_id", axis=1, inplace=True)

    # 将结果保存成 Excel 文件并提供下载
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        all_res.to_excel(writer, sheet_name='Sheet1', index=False)
        writer.close()

    download2 = st.download_button(
        label="Download data as Excel",
        data=buffer,
        file_name='因子配置.xlsx',
        mime='application/vnd.ms-excel'
    )

    # 显示结果
    st.write(all_res)


# 将数字转换为 ASCII 码对应的字符
def convert_to_ascii(s):
    return chr(int(s + 66))


# 在 Streamlit 页面上创建上传文件的选项
buffer = io.BytesIO()
file = st.file_uploader("请上传文件", type="xlsx")

# 如果有文件被上传，则读取上传的文件并调用因子配置函数
if file is not None:
    data = pd.read_excel(file, "表达式配置", dtype=str)
    xibu_factor(data)
