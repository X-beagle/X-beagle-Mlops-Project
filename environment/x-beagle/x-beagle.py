''' 
x-beagle streamlit 합본

main: 전체 틀 
detection: 판독 화면 
test: 통계 시각화 화면 
search: 과거 기록 검색
check: 체크박스

'''
import streamlit as st
import pandas as pd
from urllib.request import urlopen
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import json
import requests
from streamlit_lottie import st_lottie
import pydeck as pdk
import snowflake.connector
import os
import boto3
import zipfile
from PIL import Image
from io import BytesIO
import base64
import numpy as np
import cv2

# AWS 리전 설정 
session = boto3.Session(region_name='ap-northeast-2')

# 세이지메이커 엔드포인트 이름
endpoint_name = "xbeagle-yolov8-2024-05-21-08-57-55-167172"

# 세이지메이커 엔드포인트 URL
endpoint_url = "https://runtime.sagemaker.ap-northeast-2.amazonaws.com/endpoints/x-beagle-endpoint/invocations"

#api_url
api_url="https://jn1f1wadda.execute-api.ap-northeast-2.amazonaws.com/default/x-beagle"
lambda_endpoint_url="https://ris8pyly79.execute-api.ap-northeast-2.amazonaws.com/x_beagle/predict"

api_gateway_url = "https://jn1f1wadda.execute-api.ap-northeast-2.amazonaws.com/default/x-beagle"

# Layout
st.set_page_config(
    page_title="X-beagle",
    layout="wide",
    initial_sidebar_state="expanded")

# 파일 업로드 버튼과 date 입력 필드의 텍스트 색상 변경을 위한 CSS 스타일
st.markdown("""
    <style>
        .stFileUploader .btn, .stDateInput input {
            color: #ffffff !important;
        }
    </style>
""", unsafe_allow_html=True)

# Data Pull and Functions
st.markdown("""
<style>
.big-font {
    font-size:80px !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# 위해물품 리스트
hazardous_items_dict = {
    0: 'Hammer', 1: 'SSD', 2: 'Alcohol', 3: 'Spanner', 4: 'Axe', 5: 'Awl', 6: 'Throwing Knife', 7: 'Firecracker',
    8: 'Thinner', 9: 'Plier', 10: 'Match', 11: 'Smart Phone', 12: 'Scissors', 13: 'Tablet PC', 14: 'Solid Fuel',
    15: 'Bat', 16: 'Portable Gas', 17: 'Nail Clippers', 18: 'Knife', 19: 'Metal Pipe',
    20: 'Electronic Cigarettes(Liquid)', 21: 'Supplymentary Battery', 22: 'Bullet', 23: 'Gun Parts', 24: 'USB',
    25: 'Liquid', 26: 'Aerosol', 27: 'Screwdriver', 28: 'Chisel', 29: 'Handcuffs', 30: 'Lighter', 31: 'HDD',
    32: 'Electronic Cigarettes', 33: 'Battery', 34: 'Gun', 35: 'Laptop', 36: 'Saw', 37: 'Zippo Oil', 38: 'Stun Gun',
    39: 'Camera', 40: 'Camcorder', 41: 'SD Card'
}

# Options Menu
with st.sidebar:
    selected = option_menu('X-beagle', ["판독화면", '체크박스', '통계 시각화 화면', '과거 기록 검색'], 
        icons=['play-btn', 'bar-chart', 'search', 'check-square'], menu_icon='intersect', default_index=0)
        
# Initialize session state
if 'selected_items' not in st.session_state:
    st.session_state.selected_items = []

## 판독화면 Page ##
if selected == "판독화면":
    # Header
    st.markdown(f'<div style="line-height: 2.0;"><span style="font-size: 32pt; font-weight: bold;">판독화면</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="line-height: 2.0;"><span style="font-size: 20pt; font-weight: normal;">Xray로 촬영한 영상을 업로드하면, 위해 물품을 인식하여 보여줍니다.</span><br>', unsafe_allow_html=True)
    st.divider()


## 체크박스 Page ##

# 세션 상태 초기화
if 'selected_items' not in st.session_state:
    st.session_state.selected_items = []

if selected == '체크박스':
    st.markdown(f'<div style="line-height: 2.0;"><span style="font-size: 32pt; font-weight: bold;">위해물품 품목 설정</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="line-height: 2.0;"><span style="font-size: 20pt; font-weight: normal;">위해물품으로 탐지할 품목을 설정할 수 있는 화면입니다. 필요한 품목에만 체크 표시 해주세요.</span><br>', unsafe_allow_html=True)
    
    # 위해물품 리스트
    hazardous_items = ['Hammer', 'SSD', 'Alcohol', 'Spanner', 'Axe', 'Awl', 'Throwing Knife', 'Firecracker', 'Thinner',
             'Plier', 'Match', 'Smart Phone', 'Scissors', 'Tablet PC', 'Solid Fuel', 'Bat', 'Portable Gas',
             'Nail Clippers', 'Knife', 'Metal Pipe', 'Electronic Cigarettes(Liquid)', 'Supplementary Battery',
             'Bullet', 'Gun Parts', 'USB', 'Liquid', 'Aerosol', 'Screwdriver', 'Chisel', 'Handcuffs', 'Saw',
             'Zippo Oil', 'Stun Gun', 'Camera', 'Camcorder', 'SD Card']
    
    # 선택된 위해물품 출력
    def update_selected_items():
        selected_items_str = " / ".join(st.session_state.selected_items)
        return selected_items_str

    st.markdown("---")  # 구분선 추가
  
    selected_items_placeholder = st.empty()
    
    # 선택된 위해물품 문자열 가져오기
    selected_items_str = update_selected_items()
    
    # 선택된 위해물품 출력
    selected_items_placeholder.write(f"선택된 위해물품: {selected_items_str}")

    st.markdown("---")  # 구분선 추가
    
    # 체크박스를 4줄로 나타내기
    col1, col2, col3, col4 = st.columns(4)
    num_items = len(hazardous_items)
    num_items_per_col = (num_items + 3) // 4
    
    
    with col1:
        for item in hazardous_items[:num_items_per_col]:
            selected = st.checkbox(item, value=item in st.session_state.selected_items, key=item)
            if selected:
                if item not in st.session_state.selected_items:
                    st.session_state.selected_items.append(item)
            else:
                if item in st.session_state.selected_items:
                    st.session_state.selected_items.remove(item)
    
    with col2:
        for item in hazardous_items[num_items_per_col:num_items_per_col*2]:
            selected = st.checkbox(item, value=item in st.session_state.selected_items, key=item)
            if selected:
                if item not in st.session_state.selected_items:
                    st.session_state.selected_items.append(item)
            else:
                if item in st.session_state.selected_items:
                    st.session_state.selected_items.remove(item)
    
    with col3:
        for item in hazardous_items[num_items_per_col*2:num_items_per_col*3]:
            selected = st.checkbox(item, value=item in st.session_state.selected_items, key=item)
            if selected:
                if item not in st.session_state.selected_items:
                    st.session_state.selected_items.append(item)
            else:
                if item in st.session_state.selected_items:
                    st.session_state.selected_items.remove(item)
    
    with col4:
        for item in hazardous_items[num_items_per_col*3:]:
            selected = st.checkbox(item, value=item in st.session_state.selected_items, key=item)
            if selected:
                if item not in st.session_state.selected_items:
                    st.session_state.selected_items.append(item)
            else:
                if item in st.session_state.selected_items:
                    st.session_state.selected_items.remove(item)
    
    # 선택된 위해물품 업데이트
    selected_items_placeholder.markdown(f"**선택된 위해물품:** {update_selected_items()}")


## 통계 시각화 화면 Page ##
if selected == "통계 시각화 화면":
    st.markdown(f'<div style="line-height: 2.0;"><span style="font-size: 32pt; font-weight: bold;"> 통계 시각화</span></div>', unsafe_allow_html=True)

    # 오늘 총 몇 건의 위해 물품이 발견되었는지
    total_detections = 100  # 예시 값입니다. 실제 값으로 대체해야 합니다.
    st.markdown(f'<div style="line-height: 2.0;"><span style="font-size: 24pt; font-weight: normal;">오늘 총 {total_detections}건의 위해 물품이 발견되었습니다.</span>', unsafe_allow_html=True)


    # 위해 물품 별 탐지된 개수 그래프
    class_names = hazardous_items_dict
    
    # 각 위해 물품 별 탐지된 개수 예시 데이터
    detection_counts = {
        'Hammer': 10,
        'SSD': 5,
        'Alcohol': 8,
        'Spanner': 3,
        'Axe': 1,
        'Awl': 3,
        'Throwing Knife': 5,
        'Firecracker': 9,
        'Thinner': 10,
        'Plier': 5,
        'Match': 13
    }
    
    items = list(detection_counts.keys())
    counts = list(detection_counts.values())
    
    fig = go.Figure(data=[go.Bar(x=items, y=counts)])
    fig.update_layout(
        title='위해 물품 별 탐지된 개수',
        xaxis_title='위해 물품',
        yaxis_title='탐지된 개수'
    )
    st.plotly_chart(fig)
    
    # 시간대별 발견된 위해 물품의 개수
    hourly_detections = {
        '00:00': 5,
        '01:00': 3,
        '02:00': 2,
        '03:00': 4,
        '04:00': 6,
        '05:00': 7,
        '08:00': 10,
        '09:00': 15,
        '10:00': 12,
        '11:00': 8,
        '12:00': 20
    }
    
    hours = list(hourly_detections.keys())
    counts = list(hourly_detections.values())
    
    fig = go.Figure(data=[go.Scatter(x=hours, y=counts, mode='lines+markers')])
    fig.update_layout(
        title='시간대별 발견된 위해 물품의 개수',
        xaxis_title='시간대',
        yaxis_title='발견된 개수'
    )
    st.plotly_chart(fig)



## 과거 검색 기록 Page ##
if selected == '과거 기록 검색':
    st.markdown(f'<div style="line-height: 2.0;"><span style="font-size: 32pt; font-weight: bold;">과거 기록 검색 화면</span></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    num_items = len(hazardous_items_dict)
    num_items_per_col = (num_items + 2) // 3
    
    select_date = st.date_input(label='Date', value=pd.to_datetime("today").date())
    
    st.markdown("###### Items")
    col1, col2, col3, col4 = st.columns(4)
    
    items = ['Hammer', 'SSD', 'Alcohol', 'Spanner', 'Axe', 'Awl', 'Throwing Knife', 'Firecracker', 'Thinner',
             'Plier', 'Match', 'Smart Phone', 'Scissors', 'Tablet PC', 'Solid Fuel', 'Bat', 'Portable Gas',
             'Nail Clippers', 'Knife', 'Metal Pipe', 'Electronic Cigarettes(Liquid)', 'Supplementary Battery',
             'Bullet', 'Gun Parts', 'USB', 'Liquid', 'Aerosol', 'Screwdriver', 'Chisel', 'Handcuffs', 'Saw',
             'Zippo Oil', 'Stun Gun', 'Camera', 'Camcorder', 'SD Card']
    
    num_items_per_col = len(items) // 4

    with col1:
        for item in items[:num_items_per_col]:
            selected = st.checkbox(item, value=item in st.session_state.selected_items, key=item)
            if selected:
                if item not in st.session_state.selected_items:
                    st.session_state.selected_items.append(item)
            else:
                if item in st.session_state.selected_items:
                    st.session_state.selected_items.remove(item)

    with col2:
        for item in items[num_items_per_col:num_items_per_col * 2]:
            selected = st.checkbox(item, value=item in st.session_state.selected_items, key=item)
            if selected:
                if item not in st.session_state.selected_items:
                    st.session_state.selected_items.append(item)
            else:
                if item in st.session_state.selected_items:
                    st.session_state.selected_items.remove(item)

    with col3:
        for item in items[num_items_per_col * 2:num_items_per_col * 3]:
            selected = st.checkbox(item, value=item in st.session_state.selected_items, key=item)
            if selected:
                if item not in st.session_state.selected_items:
                    st.session_state.selected_items.append(item)
            else:
                if item in st.session_state.selected_items:
                    st.session_state.selected_items.remove(item)

    with col4:
        for item in items[num_items_per_col * 3:]:
            selected = st.checkbox(item, value=item in st.session_state.selected_items, key=item)
            if selected:
                if item not in st.session_state.selected_items:
                    st.session_state.selected_items.append(item)
            else:
                if item in st.session_state.selected_items:
                    st.session_state.selected_items.remove(item)

    image_path = 'sample_image.png'  # Use the correct path to your image
    if os.path.exists(image_path):
        st.image(image_path)
    else:
        st.error(f"Image not found at path: {image_path}")



    