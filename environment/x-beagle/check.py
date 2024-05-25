import streamlit as st
import numpy as np
from streamlit_option_menu import option_menu

# 레이아웃
st.set_page_config(
    page_title="X-beagle",
    layout="wide",
    initial_sidebar_state="expanded")

# 사이드바 메뉴
menu = ["판독화면", "통계 시각화 화면", "과거 검색 기록", "체크박스"]
with st.sidebar:
    selected_menu = option_menu("X-beagle", menu,
        icons=['play-btn', 'bar-chart', 'search', 'check-square'], menu_icon='intersect', default_index=0)

# 세션 상태 초기화
if 'selected_items' not in st.session_state:
    st.session_state.selected_items = []

# 체크박스 메뉴
if selected_menu == "체크박스":
    st.title("체크박스")
    
    # 위해물품 리스트
    hazardous_items = [
        "Aerosol", "Alcohol", "Awl", "Axe", "Bat", "Battery", "Bullet", "Camcoder",
        "Camera", "Chisel", "Electronic Cigarettes", "Electronic Cigarettes(Liquid)",
        "Firecracker", "Gun", "Gun Parts", "HDD", "HDD_External", "Hammer", "Handcuffs",
        "Knife", "Laptop", "Lighter", "Liquid", "Match", "Metal Pipe", "Nail Clippers",
        "Plier", "Portable Gas", "SD Card", "SSD", "Saw", "Scissors", "Screwdriver",
        "Smart Phone", "Solid Fuel", "Stun Gun", "Supplymentary Battery", "Tablet PC",
        "Thinner", "Throwing Knife", "USBXx", "Zippo Oil", "sccr"
    ]
    
    # 선택된 위해물품 출력
    def update_selected_items():
        selected_items_str = " / ".join(st.session_state.selected_items)
        return selected_items_str
    
    selected_items_placeholder = st.empty()
    selected_items_placeholder.markdown(f"**선택된 위해물품:** {update_selected_items()}")
    
    st.markdown("---")  # 구분선 추가
    
    # 체크박스를 3줄로 나타내기
    col1, col2, col3 = st.columns(3)
    num_items = len(hazardous_items)
    num_items_per_col = (num_items + 2) // 3
    
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
        for item in hazardous_items[num_items_per_col*2:]:
            selected = st.checkbox(item, value=item in st.session_state.selected_items, key=item)
            if selected:
                if item not in st.session_state.selected_items:
                    st.session_state.selected_items.append(item)
            else:
                if item in st.session_state.selected_items:
                    st.session_state.selected_items.remove(item)
    
    # 선택된 위해물품 업데이트
    selected_items_placeholder.markdown(f"**선택된 위해물품:** {update_selected_items()}")