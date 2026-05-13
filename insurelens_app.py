# -*- coding: utf-8 -*-
"""
삼성화재 CSM 분석 리포트
실행: streamlit run insurelens_app.py
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# ============================================================
# 페이지 설정
# ============================================================
st.set_page_config(
    page_title="삼성화재 CSM 분석 리포트",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 커스텀 CSS — 삼성화재 블루 톤
# ============================================================
st.markdown("""
<style>
    .stApp { background-color: #F0F4F8; }
    .main-header {
        background: linear-gradient(135deg, #1428A0 0%, #1F4FCC 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 16px rgba(20, 40, 160, 0.2);
    }
    .main-header h1 { color: white; margin: 0; font-size: 26px; font-weight: 700; }
    .main-header p { color: #B8D4FF; margin: 6px 0 0 0; font-size: 14px; }
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #0A1A6B 0%, #1428A0 100%);
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stMetricValue"] { color: #1428A0 !important; font-weight: bold; font-size: 28px !important; }
    [data-testid="stMetricLabel"] { color: #6B7684 !important; font-weight: 500; }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px;
        padding: 10px 20px;
        color: #6B7684;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1428A0 !important;
        color: white !important;
    }
    .stButton button {
        background-color: #1428A0;
        color: white;
        border-radius: 8px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 로고 바 (좌: 삼성화재, 우: PwC)
# ============================================================
def render_logo_bar():
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_left:
        if os.path.exists("samsung_logo.png"):
            st.image("samsung_logo.png", width=180)
        else:
            st.markdown("""
            <div style="padding:8px 0;">
                <span style="color:#1428A0; font-size:24px; font-weight:bold; letter-spacing:-1px;">SAMSUNG</span>
                <span style="color:#1428A0; font-size:14px; margin-left:8px; font-weight:500;">화재해상보험</span>
            </div>
            """, unsafe_allow_html=True)
    with col_center:
        st.markdown("""
        <div style="text-align:center; padding:8px 0;">
            <span style="color:#1428A0; font-size:13px; letter-spacing:2px; font-weight:600;">CSM ANALYSIS REPORT</span>
        </div>
        """, unsafe_allow_html=True)
    with col_right:
        if os.path.exists("pwc_logo.png"):
            ca, cb = st.columns([3, 1])
            with cb:
                st.image("pwc_logo.png", width=80)
        else:
            st.markdown("""
            <div style="text-align:right; padding:8px 0;">
                <span style="color:#DC6900; font-size:24px; font-weight:bold; letter-spacing:-1px;">pwc</span>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# 데이터 로딩
# ============================================================
@st.cache_data
def load_data():
    df = pd.read_csv('insurance_data.csv')
    df['분기'] = pd.to_datetime(df['분기'])
    df['분기라벨'] = df['분기'].dt.strftime('%y.%m')
    return df

df = load_data()

# ============================================================
# 사이드바
# ============================================================
with st.sidebar:
    st.markdown("# 🔵 삼성화재")
    st.markdown("**CSM 분석 리포트**")
    st.markdown("---")
    menu = st.radio(
        "메뉴",
        ["🏠 홈 대시보드", "📊 회사별 상세", "⚖️ 업계 비교", "🎯 종합 경쟁력", "📰 DART 공시"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("### 📅 데이터 기준일")
    st.info("2025년 3분기 (2025.09.30)")
    st.markdown("### ℹ️ 데이터 출처")
    st.markdown("- DART 전자공시")
    st.markdown("- 5대 손보사 연결재무제표")
    st.markdown("---")
    st.caption("v0.3 (Prototype)")
    st.caption("© Samsung Fire & Marine × PwC")

# ============================================================
# 화면 1: 홈 대시보드
# ============================================================
if menu == "🏠 홈 대시보드":
    render_logo_bar()
    st.markdown("""
    <div class="main-header">
        <h1>안녕하세요, IR팀 👋</h1>
        <p>2025년 3분기 실적 업데이트가 완료되었습니다</p>
    </div>
    """, unsafe_allow_html=True)
    
    samsung = df[df['회사']=='삼성화재'].sort_values('분기').reset_index(drop=True)
    samsung_valid = samsung[samsung['CSM'] > 0].iloc[-1]
    prev = samsung[samsung['CSM'] > 0].iloc[-2]
    
    st.markdown("### 📊 핵심 지표")
    col1, col2, col3, col4 = st.columns(4)
    
    csm_now, csm_prev = samsung_valid['CSM'], prev['CSM']
    csm_chg = (csm_now - csm_prev) / csm_prev * 100
    
    with col1:
        st.metric("💎 CSM 잔액", f"{csm_now/1e6:.2f}조", f"{csm_chg:+.2f}% QoQ")
    with col2:
        rate_now = samsung_valid['CSM상각률'] * 100
        rate_prev = prev['CSM상각률'] * 100
        st.metric("📈 CSM 상각률", f"{rate_now:.2f}%", f"{rate_now - rate_prev:+.2f}%p")
    with col3:
        new_now, new_prev = samsung_valid['신계약발생액'], prev['신계약발생액']
        st.metric("🆕 신계약 발생액", f"{new_now/1e3:,.0f}억",
                  f"{(new_now-new_prev)/new_prev*100:+.1f}%")
    with col4:
        latest_q = df[df['CSM'] > 0].groupby('회사')['분기'].max().reset_index()
        latest_data = df.merge(latest_q, on=['회사', '분기'])
        latest_data = latest_data.sort_values('CSM', ascending=False).reset_index(drop=True)
        rank = latest_data[latest_data['회사']=='삼성화재'].index[0] + 1
        st.metric("🏆 업계 순위", f"{rank}위 / 5사", "유지")
    
    st.markdown("---")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # ⭐ 막대그래프로 변경
        st.markdown("### 📊 삼성화재 CSM 분기 추이")
        samsung_chart = samsung[samsung['CSM'] > 0].copy()
        samsung_chart['CSM_조'] = samsung_chart['CSM'] / 1e6
        
        # 최신 분기는 진한 색, 이전은 연한 색
        bar_colors = ['#5B7FE0'] * (len(samsung_chart) - 1) + ['#1428A0']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=samsung_chart['분기라벨'],
            y=samsung_chart['CSM_조'],
            marker=dict(color=bar_colors, line=dict(color='#0A1A6B', width=1)),
            text=[f"{v:.1f}" for v in samsung_chart['CSM_조']],
            textposition='outside',
            textfont=dict(size=11, color='#1428A0'),
            hovertemplate='<b>%{x}</b><br>CSM: %{y:.2f}조<extra></extra>',
            name='CSM 잔액'
        ))
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=30, b=40),
            plot_bgcolor='white',
            yaxis=dict(title='조원', gridcolor='#E5E8EB', zeroline=True, zerolinecolor='#CED4DA'),
            xaxis=dict(gridcolor='#E5E8EB', tickangle=-45),
            showlegend=False,
            bargap=0.25
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.markdown("### 🏆 25.3Q 업계 순위")
        for i, row in latest_data.iterrows():
            rank_emoji = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i]
            highlight = "background:#E8EFFF; border-left: 4px solid #1428A0;" if row['회사']=='삼성화재' else "background:white;"
            st.markdown(f"""
            <div style="{highlight} padding:12px; margin-bottom:8px; border-radius:8px;">
                <span style="font-size:18px;">{rank_emoji}</span>
                <strong style="color:#1428A0;">{row['회사']}</strong>
                <span style="float:right; color:#1428A0; font-weight:bold;">{row['CSM']/1e6:.2f}조</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📢 최신 공시 알림")
    st.info("🔔 **삼성화재 2025년 3분기 사업보고서** — 2025.11.14 DART 공시 · 자동 반영 완료")

# ============================================================
# 화면 2: 회사별 상세
# ============================================================
elif menu == "📊 회사별 상세":
    render_logo_bar()
    st.markdown("""
    <div class="main-header">
        <h1>📊 회사별 상세 분석</h1>
        <p>5대 손해보험사 개별 분석</p>
    </div>
    """, unsafe_allow_html=True)
    
    company = st.selectbox("회사 선택", df['회사'].unique(), index=0)
    company_df = df[df['회사']==company].sort_values('분기')
    company_valid = company_df[company_df['CSM'] > 0]
    
    latest_row = company_valid.iloc[-1]
    prev_row = company_valid.iloc[-2]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("CSM 잔액", f"{latest_row['CSM']/1e6:.2f}조",
                  f"{(latest_row['CSM']-prev_row['CSM'])/prev_row['CSM']*100:+.2f}%")
    with col2:
        st.metric("신계약 발생액", f"{latest_row['신계약발생액']/1e3:,.0f}억",
                  f"{(latest_row['신계약발생액']-prev_row['신계약발생액'])/prev_row['신계약발생액']*100:+.2f}%")
    with col3:
        st.metric("CSM 상각률", f"{latest_row['CSM상각률']*100:.2f}%",
                  f"{(latest_row['CSM상각률']-prev_row['CSM상각률'])*100:+.2f}%p")
    
    tab1, tab2, tab3 = st.tabs(["📊 CSM 추이", "📊 신계약 추이", "📋 데이터 표"])
    
    with tab1:
        # ⭐ 막대그래프로 변경
        chart_data = company_valid.copy()
        chart_data['CSM_조'] = chart_data['CSM'] / 1e6
        bar_colors2 = ['#5B7FE0'] * (len(chart_data) - 1) + ['#1428A0']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=chart_data['분기라벨'],
            y=chart_data['CSM_조'],
            marker=dict(color=bar_colors2, line=dict(color='#0A1A6B', width=1)),
            text=[f"{v:.2f}" for v in chart_data['CSM_조']],
            textposition='outside',
            textfont=dict(size=11, color='#1428A0'),
            hovertemplate='<b>%{x}</b><br>CSM: %{y:.2f}조<extra></extra>',
            name='CSM 잔액'
        ))
        fig.update_layout(
            height=420,
            plot_bgcolor='white',
            yaxis=dict(title='조원', gridcolor='#E5E8EB'),
            xaxis=dict(title='분기', tickangle=-45, gridcolor='#E5E8EB'),
            margin=dict(l=20, r=20, t=30, b=40),
            bargap=0.25,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=company_valid['분기라벨'],
            y=company_valid['신계약발생액']/1e3,
            marker_color='#1F4FCC',
            name='신계약 발생액'
        ))
        fig.update_layout(height=400, plot_bgcolor='white',
                          yaxis_title='억원', xaxis_title='분기',
                          margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        display_df = company_valid[['분기라벨','CSM','신계약발생액','CSM상각액','CSM상각률']].copy()
        display_df.columns = ['분기','CSM(백만원)','신계약(백만원)','상각액(백만원)','상각률']
        display_df['상각률'] = display_df['상각률'].apply(lambda x: f"{x*100:.2f}%")
        st.dataframe(display_df, use_container_width=True, hide_index=True)

# ============================================================
# 화면 3: 업계 비교
# ============================================================
elif menu == "⚖️ 업계 비교":
    render_logo_bar()
    st.markdown("""
    <div class="main-header">
        <h1>⚖️ 업계 비교 분석</h1>
        <p>5대 손해보험사 동시 비교 — 핵심 차별화 기능 ⭐</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_companies = st.multiselect(
            "비교할 회사 선택",
            df['회사'].unique().tolist(),
            default=df['회사'].unique().tolist()
        )
    with col2:
        metric_choice = st.selectbox("비교 지표", ['CSM', '신계약발생액', 'CSM상각액', 'CSM상각률'])
    
    if selected_companies:
        compare_df = df[df['회사'].isin(selected_companies) & (df['CSM'] > 0)]
        
        st.markdown(f"### 📈 {metric_choice} 분기 추이 비교")
        colors = {
            '삼성화재':'#1428A0',
            'DB손해보험':'#FF6B35',
            '메리츠화재':'#06A77D',
            '현대해상':'#7B61FF',
            'KB손해보험':'#FFB800'
        }
        
        fig = go.Figure()
        for company in selected_companies:
            cdf = compare_df[compare_df['회사']==company].sort_values('분기')
            y = cdf[metric_choice]
            if metric_choice == 'CSM상각률':
                y = y * 100
            elif metric_choice == 'CSM':
                y = y / 1e6
            else:
                y = y / 1e3
            line_width = 4 if company == '삼성화재' else 2
            fig.add_trace(go.Scatter(
                x=cdf['분기라벨'], y=y,
                mode='lines+markers',
                name=company,
                line=dict(color=colors.get(company, '#888'), width=line_width),
                marker=dict(size=8 if company=='삼성화재' else 6)
            ))
        unit = '%' if metric_choice == 'CSM상각률' else ('조원' if metric_choice=='CSM' else '억원')
        fig.update_layout(height=450, plot_bgcolor='white',
                          yaxis_title=unit, xaxis_title='분기',
                          margin=dict(l=20, r=20, t=20, b=20),
                          legend=dict(orientation='h', y=-0.15))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"### 🏆 최신 분기 {metric_choice} 순위")
        latest_q = compare_df.groupby('회사')['분기'].max().reset_index()
        latest_compare = compare_df.merge(latest_q, on=['회사','분기'])
        latest_compare = latest_compare.sort_values(metric_choice, ascending=True)
        
        y_vals = latest_compare[metric_choice]
        if metric_choice == 'CSM상각률':
            y_vals = y_vals * 100
        elif metric_choice == 'CSM':
            y_vals = y_vals / 1e6
        else:
            y_vals = y_vals / 1e3
        
        fig2 = go.Figure(go.Bar(
            x=y_vals, y=latest_compare['회사'],
            orientation='h',
            marker_color=[colors.get(c, '#888') for c in latest_compare['회사']],
            text=[f"{v:.2f}{unit}" for v in y_vals],
            textposition='outside'
        ))
        fig2.update_layout(height=350, plot_bgcolor='white',
                           xaxis_title=unit,
                           margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig2, use_container_width=True)

# ============================================================
# 화면 4: 종합 경쟁력
# ============================================================
elif menu == "🎯 종합 경쟁력":
    render_logo_bar()
    st.markdown("""
    <div class="main-header">
        <h1>🎯 종합 경쟁력 분석</h1>
        <p>삼성화재 vs 업계평균 — 5대 지표 레이더 분석</p>
    </div>
    """, unsafe_allow_html=True)
    
    latest_data = df[df['CSM'] > 0].groupby('회사').apply(lambda x: x.sort_values('분기').iloc[-1]).reset_index(drop=True)
    
    metrics_for_radar = ['CSM', '신계약발생액', 'CSM상각률', '유입현금흐름대비신계약비율']
    radar_df = latest_data[['회사'] + metrics_for_radar].copy()
    
    for m in metrics_for_radar:
        radar_df[m] = (radar_df[m] - radar_df[m].min()) / (radar_df[m].max() - radar_df[m].min())
    
    categories = ['CSM 규모', '신계약 발생', 'CSM 상각률', '신계약 비율']
    
    fig = go.Figure()
    samsung_vals = radar_df[radar_df['회사']=='삼성화재'][metrics_for_radar].values[0].tolist()
    industry_avg = radar_df[metrics_for_radar].mean().tolist()
    
    fig.add_trace(go.Scatterpolar(
        r=samsung_vals + [samsung_vals[0]],
        theta=categories + [categories[0]],
        fill='toself', name='삼성화재',
        line=dict(color='#1428A0', width=3),
        fillcolor='rgba(20, 40, 160, 0.3)'
    ))
    fig.add_trace(go.Scatterpolar(
        r=industry_avg + [industry_avg[0]],
        theta=categories + [categories[0]],
        fill='toself', name='업계 평균',
        line=dict(color='#FF6B35', width=2, dash='dash'),
        fillcolor='rgba(255, 107, 53, 0.15)'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        height=500, showlegend=True,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 💡 자동 분석 인사이트")
    samsung_score = sum(samsung_vals) / len(samsung_vals)
    avg_score = sum(industry_avg) / len(industry_avg)
    
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"✅ **삼성화재 종합 점수**: {samsung_score*100:.1f}점")
    with col2:
        st.info(f"📊 **업계 평균 점수**: {avg_score*100:.1f}점")
    
    if samsung_vals[0] > industry_avg[0]:
        st.markdown("- ✓ **CSM 규모**가 업계 평균을 상회하며 시장 지배력을 유지")
    if samsung_vals[1] < industry_avg[1]:
        st.markdown("- ⚠ **신계약 발생액**은 일부 경쟁사 대비 둔화 — 신규 영업 강화 검토 필요")
    
    st.markdown("---")
    if st.button("📤 보고서 PDF로 공유하기", use_container_width=True):
        st.success("PDF 생성 기능은 정식 개발 시 구현 예정입니다")

# ============================================================
# 화면 5: DART 공시
# ============================================================
elif menu == "📰 DART 공시":
    render_logo_bar()
    st.markdown("""
    <div class="main-header">
        <h1>📰 DART 공시 알림</h1>
        <p>전자공시시스템 자동 연동</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 정식 버전에서는 **DART OpenAPI**를 통해 실시간 공시 자동 수집 예정")
    
    notices = [
        {"date":"2025-11-14", "company":"삼성화재", "title":"분기보고서 (2025.09)", "type":"정기공시"},
        {"date":"2025-11-13", "company":"DB손해보험", "title":"분기보고서 (2025.09)", "type":"정기공시"},
        {"date":"2025-11-12", "company":"메리츠화재", "title":"분기보고서 (2025.09)", "type":"정기공시"},
        {"date":"2025-11-08", "company":"삼성화재", "title":"주요사항보고서 (자기주식취득)", "type":"수시공시"},
        {"date":"2025-10-30", "company":"현대해상", "title":"분기보고서 (2025.09)", "type":"정기공시"},
    ]
    
    for n in notices:
        with st.container():
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                st.caption(n['date'])
            with col2:
                st.markdown(f"**{n['company']}** — {n['title']}")
                st.caption(f"📌 {n['type']}")
            with col3:
                st.markdown("[원문 →](https://dart.fss.or.kr)")
            st.markdown("---")
