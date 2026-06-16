import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from physics.poiseuille import flow_rate

from models.straight import simulate as straight_model
from models.curved import simulate as curved_model
from models.branch import simulate as branch_model

from visualization.plots import vessel_plot

from utils.sensitivity import sensitivity_curve

st.set_page_config(
    layout="wide"
)

st.title(
    "약물 전달 경로 시뮬레이션"
)

# ====================
# Sidebar
# ====================

st.sidebar.header(
    "파라미터"
)

vessel_type = st.sidebar.selectbox(
    "혈관 구조",
    [
        "직선형",
        "곡선형",
        "분기형"
    ]
)

r = st.sidebar.slider(
    "혈관 반지름 r",
    0.5,
    5.0,
    2.0,
    0.1
)

eta = st.sidebar.slider(
    "점성 η",
    0.1,
    10.0,
    1.0,
    0.1
)

# ====================
# 모델 선택
# ====================

if vessel_type == "직선형":

    result = straight_model()

elif vessel_type == "곡선형":

    a = st.sidebar.slider(
        "곡률 a",
        0.0,
        0.5,
        0.1,
        0.01
    )

    result = curved_model(a)

else:

    theta = st.sidebar.slider(
        "분기각 θ",
        10,
        120,
        60
    )

    result = branch_model(theta)

# ====================
# 계산
# ====================

Q = flow_rate(
    r,
    eta,
    result["L"]
)

A_score = result["A"]

D_score = result["D"]

E = (
    Q
    *
    A_score
    *
    D_score
)

# ====================
# Layout
# ====================

col1, col2 = st.columns(
    [2, 1]
)

with col1:

    fig = vessel_plot(
        result["x"],
        result["y"],
        result["Fx"],
        result["Fy"]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.metric(
        "유량 Q",
        f"{Q:.4f}"
    )

    st.metric(
        "방향성 A",
        f"{A_score:.4f}"
    )

    st.metric(
        "분포성 D",
        f"{D_score:.4f}"
    )

    st.metric(
        "전달효율 E",
        f"{E:.4f}"
    )

# ====================
# 민감도 분석
# ====================

st.header(
    "반지름 변화에 따른 전달효율"
)

r_values, E_values = sensitivity_curve(
    eta,
    result["L"],
    A_score,
    D_score
)

fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=r_values,
        y=E_values,
        mode="lines"
    )
)

fig2.update_layout(
    xaxis_title="반지름 r",
    yaxis_title="전달효율 E",
    height=500
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ====================
# 데이터 테이블
# ====================

df = pd.DataFrame({
    "Q": [Q],
    "A": [A_score],
    "D": [D_score],
    "E": [E]
})

st.subheader(
    "계산 결과"
)

st.dataframe(
    df,
    use_container_width=True
)