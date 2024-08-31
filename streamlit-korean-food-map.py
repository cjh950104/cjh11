import streamlit as st
import folium
from streamlit_folium import folium_static
import random
from geopy.distance import geodesic

# 가상의 장소 데이터 생성 함수
def generate_places_data():
    return [
        {"name": "경복궁", "type": "관광지", "location": [37.579617, 126.977041], "description": "조선 왕조의 법궁", "rating": 4.5},
        {"name": "명동교자", "type": "맛집", "location": [37.563431, 126.984931], "description": "유명한 칼국수 맛집", "rating": 4.3},
        {"name": "남산서울타워", "type": "관광지", "location": [37.551111, 126.988333], "description": "서울의 상징적인 타워", "rating": 4.4},
        {"name": "광장시장", "type": "맛집", "location": [37.570087, 126.999252], "description": "다양한 길거리 음식", "rating": 4.2},
        {"name": "북촌한옥마을", "type": "관광지", "location": [37.582636, 126.983863], "description": "전통 한옥 마을", "rating": 4.1},
        {"name": "을지로 골뱅이", "type": "맛집", "location": [37.566005, 126.992598], "description": "유명한 골뱅이 무침", "rating": 4.0},
        {"name": "창덕궁", "type": "관광지", "location": [37.579389, 126.991033], "description": "유네스코 세계문화유산", "rating": 4.6},
        {"name": "통인시장", "type": "맛집", "location": [37.579784, 126.969962], "description": "도시락 카페 거리", "rating": 4.0},
        {"name": "덕수궁", "type": "관광지", "location": [37.565833, 126.975000], "description": "서양식 건물이 있는 궁궐", "rating": 4.3},
        {"name": "광화문 곱창", "type": "맛집", "location": [37.572530, 126.976900], "description": "인기 있는 곱창 전문점", "rating": 4.2},
        {"name": "청계천", "type": "관광지", "location": [37.569468, 126.978673], "description": "도심 속 휴식 공간", "rating": 4.2},
        {"name": "종로 삼겹살", "type": "맛집", "location": [37.572490, 126.991209], "description": "유명한 삼겹살 골목", "rating": 4.1},
        {"name": "인사동", "type": "관광지", "location": [37.574220, 126.983774], "description": "전통 문화의 중심지", "rating": 4.0},
        {"name": "명동 칼국수", "type": "맛집", "location": [37.563128, 126.986182], "description": "40년 전통의 칼국수", "rating": 4.4},
        {"name": "남대문시장", "type": "관광지", "location": [37.559881, 126.977700], "description": "서울 최대의 전통시장", "rating": 4.0}
    ]

# 근처 장소 찾기 함수
def get_nearby_places(lat, lon, places, max_distance=3):
    return [place for place in places if geodesic((lat, lon), tuple(place["location"])).km <= max_distance]

# 데이트 코스 생성 함수
def generate_date_course(places):
    attractions = [place for place in places if place["type"] == "관광지"]
    restaurants = [place for place in places if place["type"] == "맛집"]
    
    course = []
    if attractions:
        course.append(random.choice(attractions))
    if restaurants:
        course.append(random.choice(restaurants))
    if len(attractions) > 1:
        course.append(random.choice([a for a in attractions if a != course[0]]))
    
    return course

# Streamlit 앱 시작
st.title("한국 맛집 & 관광지 지도")

# 사이드바에 검색 기능 추가
search_query = st.sidebar.text_input("지역 검색")

# AI 추천 버튼
if st.sidebar.button("AI 추천"):
    recommendation_location = st.sidebar.text_input("어떤 지역의 데이트 코스를 추천해드릴까요?")
    if recommendation_location:
        # 실제로는 여기서 지오코딩을 수행해야 합니다.
        # 간단한 예시를 위해 서울 중심 좌표를 사용합니다.
        center_lat, center_lon = 37.5665, 126.9780
        nearby_places = get_nearby_places(center_lat, center_lon, generate_places_data())
        date_course = generate_date_course(nearby_places)
        
        st.sidebar.subheader(f"{recommendation_location} 주변 데이트 코스 추천")
        for i, place in enumerate(date_course, 1):
            st.sidebar.write(f"{i}. {place['name']} ({place['type']})")

# 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 장소 데이터 가져오기
places = generate_places_data()

# 지도에 마커 추가
for place in places:
    popup_content = f"""
    <div style="width: 200px;">
        <h4>{place['name']}</h4>
        <p><strong>종류:</strong> {place['type']}</p>
        <p>{place['description']}</p>
        <p><strong>별점:</strong> {place['rating']} / 5</p>
    </div>
    """
    icon_color = 'red' if place['type'] == '관광지' else 'blue'
    folium.Marker(
        place['location'],
        popup=popup_content,
        tooltip=place['name'],
        icon=folium.Icon(color=icon_color)
    ).add_to(m)

# Streamlit에 지도 표시
folium_static(m)

# 필터링 옵션
st.sidebar.subheader("필터")
place_type = st.sidebar.multiselect("장소 유형", options=["맛집", "관광지"])
min_rating = st.sidebar.slider("최소 별점", 0.0, 5.0, 0.0, 0.1)

# 필터링된 장소 목록 표시
filtered_places = [
    place for place in places
    if (not place_type or place["type"] in place_type) and place["rating"] >= min_rating
]

st.subheader("필터링된 장소 목록")
for place in filtered_places:
    st.write(f"{place['name']} - {place['type']} (별점: {place['rating']})")
    st.write(place['description'])
    st.write("---")
