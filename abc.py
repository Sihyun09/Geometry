import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# =====================================
# 페이지 설정
# =====================================

st.set_page_config(layout="wide")

st.title("약물 전달 경로 시뮬레이션")

# =====================================
# 사이드바
# =====================================

st.sidebar.header("파라미터")

vessel_type = st.sidebar.selectbox(
    "혈관 구조",
    ["직선형", "곡선형", "분기형"]
)

# 공통 파라미터

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

# 사용 여부(Boolean)

show_curvature = (vessel_type == "곡선형")
show_branch_angle = (vessel_type == "분기형")

# 기본값

a = 0.1
theta_deg = 60

# 곡선형 전용

if show_curvature:

    a = st.sidebar.slider(
        "곡률 a",
        0.0,
        0.5,
        0.1,
        0.01
    )

# 분기형 전용

if show_branch_angle:

    theta_deg = st.sidebar.slider(
        "분기각 θ",
        10,
        120,
        60
    )

# =====================================
# 공통 설정
# =====================================

g = np.array([1, 0])

# =====================================
# 직선형
# =====================================

if vessel_type == "직선형":

    A_pt = np.array([0, 0])
    B_pt = np.array([10, 0])

    v = B_pt - A_pt

    L = np.linalg.norm(v)

    A_score = (
        np.dot(v, g)
        /
        (np.linalg.norm(v) * np.linalg.norm(g))
    )

    D_score = 1.0

    x = [0, 10]
    y = [0, 0]

# =====================================
# 곡선형
# =====================================

elif vessel_type == "곡선형":

    x_curve = np.linspace(0, 10, 100)

    y_curve = a * (x_curve - 5) ** 2

    vecs = np.column_stack([
        np.diff(x_curve),
        np.diff(y_curve)
    ])

    cosines = []
    lengths = []

    for vec in vecs:

        cosines.append(
            np.dot(vec, g)
            /
            np.linalg.norm(vec)
        )

        lengths.append(
            np.linalg.norm(vec)
        )

    A_score = np.mean(cosines)

    L = np.sum(lengths)

    D_score = (
        1
        +
        (max(y_curve) - min(y_curve)) / 10
    )

    x = x_curve
    y = y_curve

# =====================================
# 분기형
# =====================================

else:

    theta = np.radians(theta_deg)

    S = np.array([0, -4])
    C = np.array([5, -4])

    B1 = C + 5 * np.array([
        np.cos(theta / 2),
        np.sin(theta / 2)
    ])

    B2 = C + 5 * np.array([
        np.cos(theta / 2),
        -np.sin(theta / 2)
    ])

    v = B1 - C

    A_score = (
        np.dot(v, g)
        /
        np.linalg.norm(v)
    )

    D_score = (
        1
        +
        np.linalg.norm(B1 - B2) / 10
    )

    L = (
        np.linalg.norm(C - S)
        +
        np.linalg.norm(B1 - C)
    )

    x = [
        S[0], C[0], B1[0],
        None,
        C[0], B2[0]
    ]

    y = [
        S[1], C[1], B1[1],
        None,
        C[1], B2[1]
    ]

# =====================================
# 푸아죄유 기반 유량
# =====================================

Q = (
    np.pi * r**4
    /
    (8 * eta * L)
)

# 전달 효율

E = Q * A_score * D_score

# =====================================
# 결과 표시
# =====================================

col1, col2 = st.columns([2, 1])

with col1:

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            line=dict(width=6)
        )
    )

    fig.update_layout(
        title="혈관 구조",
        height=600,
        showlegend=False
    )

    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.metric("유량 Q", f"{Q:.4f}")
    st.metric("방향성 A", f"{A_score:.4f}")
    st.metric("분포성 D", f"{D_score:.4f}")
    st.metric("전달효율 E", f"{E:.4f}")

# =====================================
# 민감도 분석
# =====================================

st.header("반지름 변화에 따른 전달효율")

r_values = np.linspace(
    0.5,
    5,
    100
)

E_values = []

for rr in r_values:

    QQ = (
        np.pi * rr**4
        /
        (8 * eta * L)
    )

    EE = QQ * A_score * D_score

    E_values.append(EE)

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

# =====================================
# 데이터 테이블
# =====================================

df = pd.DataFrame({
    "Q": [Q],
    "A": [A_score],
    "D": [D_score],
    "E": [E]
})

st.subheader("계산 결과")

st.dataframe(
    df,
    use_container_width=True
)