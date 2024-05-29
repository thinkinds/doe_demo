import streamlit as st
import pandas as pd
import build
from numpy import NaN

method_mapping = {
    '全析因': build.build_full_fact,
    '部分析因': build.build_frac_fact_res,
    'plackett_burman': build.build_plackett_burman,
    'sukharev': build.build_sukharev,
    'box_behnken': build.build_box_behnken,
    '中心复合': build.build_central_composite,
    '拉丁方': build.build_lhs,
    '空间填充拉丁方': build.build_space_filling_lhs,
    '随机k均值聚类': build.build_random_k_means,
    '极大极小重建': build.build_maximin,
    'halton伪随机': build.build_halton,
    '均匀分布': build.build_uniform_random

}

st.title('实验设计Design of Experiment')
st.markdown('''
本demo实现的功能是，用户输入因子和水平，选择具体的实验设计方法后，程序自动生成实验设计表格。
''')

st.markdown('## 因子和水平')
experiment_data = {'Pressure': [40, 55, 70],
                   'Temperature': [290, 320, 350],
                   'Flow rate': [0.2, 0.4],
                   'Time': [5, 8]}
# 确定最长数组的长度
max_length = max(len(lst) for lst in experiment_data.values())

# 使用列表推导式截断或填充数组
aligned_data = {
    k: (v + [NaN] * (max_length - len(v))) if len(v) < max_length else v[:max_length]
    for k, v in experiment_data.items()
}

df_experiment_data = pd.DataFrame(aligned_data)
st.dataframe(df_experiment_data, hide_index=True)

st.markdown('## 选择设计方法')
with st.form(key='method_select'):
    method_str = st.selectbox('请选择一个设计方法',
                              ['全析因', '部分析因', 'plackett_burman', 'sukharev',
                               'box_behnken', '中心复合', '拉丁方', '空间填充拉丁方',
                               '随机k均值聚类', '极大极小重建', 'halton伪随机', '均匀分布'
                               ])
    submit = st.form_submit_button('生成设计')

method_func = method_mapping[method_str]
st.markdown('## 实验设计表格')
if submit is True:
    df_doe_table = method_func(experiment_data)
    st.dataframe(df_doe_table)
