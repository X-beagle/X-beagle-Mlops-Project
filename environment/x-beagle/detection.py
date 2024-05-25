import streamlit as st
import cv2
import numpy as np
import tempfile
from streamlit_option_menu import option_menu  # 모듈 불러오기
import logging
import os
import json
import requests
from streamlit_lottie import st_lottie


# 업로드된 영상 파일을 저장할 디렉토리
UPLOAD_FOLDER = 'uploads'

# 업로드된 영상 파일 목록을 저장할 리스트
uploaded_videos = []

# Layout
st.set_page_config(
    page_title="X-beagle",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Data Pull and Functions
st.markdown("""
<style>
.big-font {
    font-size:80px !important;
}
.uploaded-images-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 20px;
}
.uploaded-image {
    border: 2px solid #ccc;
    padding: 5px;
    border-radius: 5px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Options Menu
with st.sidebar:
    selected = option_menu('X-beagle', ["판독화면", '통계 시각화 화면', '과거 검색 기록', '체크박스'], 
        icons=['play-btn', 'bar-chart', 'search', 'check-square'], menu_icon='intersect', default_index=0)

# 판독화면 Page
if selected == "판독화면":
    # Header
    st.subheader('Xray로 촬영한 영상을 업로드하면, 위해 물품을 인식하여 보여줍니다.')

    st.divider()

    # 영상 업로드 기능
    st.subheader('영상 업로드')
    uploaded_files = st.file_uploader("Video", type=['mp4', 'mov'], accept_multiple_files=True)

    if uploaded_files:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 디렉토리 생성
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name
            # 파일을 업로드 디렉토리에 저장
            with open(os.path.join(UPLOAD_FOLDER, file_name), 'wb') as f:
                f.write(uploaded_file.getvalue())
            # 업로드된 파일 목록에 추가
            uploaded_videos.append((uploaded_file, file_name))

    st.divider()
    if uploaded_videos:
        st.subheader('영상 미리보기')
        cols = st.columns(4)
        for idx, (video, video_name) in enumerate(uploaded_videos):
            col = cols[idx % 4]
            col.write(video_name)
            col.video(video)
        st.divider()
        st.subheader('위험 물품 탐지 결과')


# Lambda 함수의 API Gateway URL을 설정합니다.
lambda_url = "https://gzoiwtzjxa.execute-api.ap-northeast-2.amazonaws.com/x-beagle_streamlit3"

# Lambda 함수에서 반환된 동영상 URL을 가져옵니다.
def get_video_url():
    try:
        response = requests.get(lambda_url)
        if response.status_code == 200:
            data = response.json()
            return data.get('url')
        else:
            st.error(f"Failed to retrieve video URL. Status code: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit 애플리케이션
st.title("S3 Video Streamer")

# 직접 URL을 하드코딩하여 동영상을 스트리밍합니다.
# 이 부분을 통해 Streamlit이 동영상을 올바르게 표시하는지 확인합니다.
st.video("https://x-beagle.s3.ap-northeast-2.amazonaws.com/video/test1.mp4")


        # YOLO 모델을 사용한 위험 물품 탐지 (추후에 추가할 부분)
        # for idx, (video, video_name) in enumerate(uploaded_videos):
        #     # YOLO 모델을 사용하여 객체 감지 수행
        #     results = yolo_model(video.name)
        #     detections = results.pandas().xyxy[0]  # 감지된 객체들의 정보
        #
        #     if not detections.empty:
        #         st.write(f"Detected Objects in {video_name}:")
        #         for _, det in detections.iterrows():
        #             st.write(f"{det['name']}: {det['confidence']:.2f}")


# 통계 시각화 화면 Page
if selected == "통계 시각화 화면":
    st.subheader('통계 시각화 화면 입니다.')

# 과거 검색 기록 Page
if selected == '과거 검색 기록':
    st.title('과거 검색 기록 화면입니다.')

# 체크박스 Page
if selected == '체크박스':
    st.title('체크박스 화면입니다.')