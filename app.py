import streamlit as st
import yfinance as yf
import feedparser
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="종합 주가 & 뉴스 대시보드", layout="wide")
st.title("📊 AI & 반도체 기업 실시간 대시보드")

stocks = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "마음AI": "377480.KQ",
    "비아이매트릭스": "413640.KQ"
}

def get_news(keyword):
    url = f"https://news.google.com/rss/search?q={keyword}&hl=ko&gl=KR&ceid=KR:ko"
    feed = feedparser.parse(url)
    return feed.entries[:5]

st.subheader("📌 주요 종목 현재가 요약")
cols = st.columns(len(stocks))

for i, (name, ticker) in enumerate(stocks.items()):
    data = yf.Ticker(ticker).history(period="2d")
    if not data.empty:
        curr_p = data['Close'].iloc[-1]
        prev_p = data['Close'].iloc[-2]
        delta = curr_p - prev_p
        cols[i].metric(label=name, value=f"{curr_p:,.0f}원", delta=f"{delta:,.0f}원")

st.divider()
col1, col2 = st.columns([3, 2])

with col1:
    selected_stock = st.selectbox("상세 정보를 확인하고 싶은 기업을 선택하세요.", list(stocks.keys()))
    ticker_symbol = stocks[selected_stock]
    
    st.subheader(f"📈 {selected_stock} 주가 흐름 (최근 1개월)")
    df = yf.Ticker(ticker_symbol).history(period="1mo")
    st.line_chart(df['Close'])

with col2:
    st.subheader(f"📰 {selected_stock} 최신 관련 뉴스")
    news_list = get_news(selected_stock)
    if news_list:
        for entry in news_list:
            st.markdown(f"**[{entry.title}]({entry.link})**")
            st.write(f"발행일: {entry.published}")
            st.write("---")
    else:
        st.write("관련 뉴스를 찾을 수 없습니다.")

st.info(f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (실시간 데이터 연동 중)")
