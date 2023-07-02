import streamlit as st

# markdown
st.markdown('技术是一张无形的纸，而创造则是用心书写的墨，唯有将二者相结合，方能绘就令人惊叹的艺术之作。')

# 设置网页标题
st.title('聚源数据工具')

# 展示一级标题
st.header('1. 介绍')
st.subheader('1.1 PDF类工具')
st.info('Pdf注释导出')
code1 = '''1、上传带有注释的Pdf
2、页面上会自动识别注释所在的页码、注释内容、回复内容、创建时间……。
3、页码上提供可下载的Excel文件。
'''
st.code(code1, language='text/plain')

st.subheader('1.2 Excel类工具')
st.info("西部因子配置生成")
code2 = '''1、上传西部证券的表达式配置
2、页面上自生成西部的因子配置表
3、页码上提供可下载的Excel文件。
'''
st.code(code2, language='text/plain')