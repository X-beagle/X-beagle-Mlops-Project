# AIRPORT X-RAY AI DETECTION 
공힝 X-Ray 데이터셋을 활용한 YOLO 디텍션 서비스
<br>
<br>

# ❗️ Introduction
X-Ray 데이터셋을 활용하여 AI/ML 및 클라우드 기술을 통한 YOLO 디텍션 Streamlit 애플리케이션 서비스 구현

### 💡 intention
> ① 탐지 데이터의 정확도 향상 <br/>
② 에러 발생 탐지 기술에 심층적인 통찰력을 활용 <br/> 


<br>

# 📝 시나리오
1. 고위험 물품이 탐지되면 **EventBridge**에서 **Lambda**를 호출하여 **Amazon SNS**를 통해 사용자 화면에 알림을 띄우는 시스템
2. **S3 버킷**에 저장된 정확도가 낮은 데이터를 매주 일요일마다 **EventBridge**를 통해 트리거를 발생시켜 **Sagemaker**의 학습 파이프라인이 자동으로 실행되도록 설정

<br>

<br>
<br>

# 🛠 Project Architecture
![SoftWareArchitecture](https://github.com/X-beagle/X-beagle-Mlops-Project/assets/80513699/de170b0e-c1d5-40a0-8c9d-76b1704489cc)

<br>
<br>



![3](https://github.com/user-attachments/assets/09e0a2dc-095d-40a3-8491-ef51f23c76ea)



![4](https://github.com/user-attachments/assets/71f382f2-7e6c-4ffc-9cfa-1dcd3cf2340a)
![5](https://github.com/user-attachments/assets/8c066c03-3041-4a2f-a30b-730f4fe30286)
![6](https://github.com/user-attachments/assets/85ebf5e1-9572-4546-a6c5-26ad55d95e6a)
![7](https://github.com/user-attachments/assets/b3df1690-d795-41d2-9433-a4cfa31348af)
![8](https://github.com/user-attachments/assets/b8dafcd6-8818-4138-a90a-d94750ef2f6f)
![9](https://github.com/user-attachments/assets/8a4a632a-da43-49bf-9ba0-cba20fc99e71)
![10](https://github.com/user-attachments/assets/5638d745-b3a5-4dbe-b908-4700528e306e)
![11](https://github.com/user-attachments/assets/d2207d05-92fa-4d5c-8e53-42296636b0bd)
![12](https://github.com/user-attachments/assets/089def8b-cc1c-452e-a781-3d0bff9e36ef)
![13](https://github.com/user-attachments/assets/4d9c90c4-a51b-44e0-8793-fa32b0cdbca4)
![14](https://github.com/user-attachments/assets/e219a3fc-fecf-4113-a6ed-6aeb3c3b2bb8)
![15](https://github.com/user-attachments/assets/dc1b51cd-dc89-4bf3-996b-8dab03dece85)
![16](https://github.com/user-attachments/assets/b9493abe-7e3d-4e6d-9cdc-9ca45aae7827)
![17](https://github.com/user-attachments/assets/3a5423ae-563d-4e6f-8753-926b013a8db9)
<br>

https://github.com/user-attachments/assets/1bf649de-6edf-4126-80fc-b84c0c8a830f


![18](https://github.com/user-attachments/assets/55c5384d-4cb3-4917-b716-9a32cf19ef02)

<br>

<br>

# Contributors


| Developer | Developer | Developer | Developer | Developer |
|:----------:|:----------:|:----------:|:----------:|:----------:|
| [<img src="https://avatars.githubusercontent.com/u/164169820?v=4" alt="" style="width:100px;100px;">](https://github.com/hyojung167)<br/><div align="center">김효정</div> | [<img src="https://avatars.githubusercontent.com/u/82037889?v=4" alt="" style="width:100px;100px;">](https://github.com/sseoni)<br/><div align="center">신서현</div> | [<img src="https://avatars.githubusercontent.com/u/80513699?v=4" alt="" style="width:100px;100px;">](https://github.com/ahyeon-github) <br/><div align="center">임아현</div> | [<img src="https://avatars.githubusercontent.com/u/130418732?v=4" alt="" style="width:100px;100px;">](https://github.com/chesso-o) <br/><div align="center">최서연</div> | [<img src="https://avatars.githubusercontent.com/u/93801149?v=4" alt="" style="width:100px;100px;">](https://github.com/esc-beep) <br/><div align="center">최은소</div> |
