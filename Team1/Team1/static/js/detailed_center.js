                
        // 탭 기능 구현
        document.getElementById('infoTab').addEventListener('click', function() {
            document.getElementById('infoContent').classList.add('active');
            document.getElementById('scheduleContent').classList.remove('active');
            this.classList.add('active');
            document.getElementById('scheduleTab').classList.remove('active');
        });

        document.getElementById('scheduleTab').addEventListener('click', function() {
            document.getElementById('scheduleContent').classList.add('active');
            document.getElementById('infoContent').classList.remove('active');
            this.classList.add('active');
            document.getElementById('infoTab').classList.remove('active');

            // 스케줄 데이터를 로드하는 함수 호출
            loadScheduleData();
        });

        function loadScheduleData() {
            const centerId = document.getElementById('centerInfo').getAttribute('data-center-id');
            console.log('centerId:', centerId);

            fetch(`/mainPage/get_schedule/${centerId}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Schedule data:', data);  // 데이터를 출력해 무엇을 받았는지 확인합니다.

                    const scheduleList = document.getElementById('scheduleList');
                    scheduleList.innerHTML = ''; // 이전 스케줄 항목들 제거

                    if (data.length === 0) {
                        scheduleList.innerHTML = '<li>스케줄이 없습니다.</li>';
                    } else {
                        data.forEach(item => {
                            console.log('Item:', item);  // 각 item의 구조를 확인하기 위해 출력

                            const listItem = document.createElement('li');
                            //추가
                            listItem.classList.add('scheduleList'); // 스타일 적용
                            //추가
                            const itemDiv = document.createElement('div');
                            itemDiv.classList.add('scheduleItem'); // CSS 클래스를 추가

                            listItem.innerHTML = `
                                <div>
                                    <strong>${item.time}</strong> - ${item.detail} - ${item.credit_num} 크레딧
                                    <br> ${item.duration}분 ${item.teacher} 강사
                                    <button onclick="openReservationForm('${item.id}', '${item.time}', '${item.detail}', '${item.credit_num}', '${item.teacher}', '${item.duration}')">예약</button>
                                </div>
                            `;
                            //아래 한줄 추가
                            itemDiv.appendChild(listItem);
                            scheduleList.appendChild(listItem);
                        });
                    }
                })
                .catch(error => {
                    console.error('Error loading schedule:', error);
                    document.getElementById('scheduleList').innerHTML = '<li>스케줄을 불러오는 중 오류가 발생했습니다.</li>';
                });
                }


                function openReservationForm(classId, time, detail, creditNum, teacher, duration) {
                    if (!classId) {
                        console.error("classId is undefined or null");
                        return;
                    }
                    const url = `/mainPage/reservation/?classId=${classId}&time=${time}&detail=${detail}&creditNum=${creditNum}&teacher=${teacher}&duration=${duration}`;
                    window.location.href = url;
            }

        var centerLat = "{{ center.latitude }}";
        var centerLng = "{{ center.longitude }}";

        // 카카오맵 API를 사용한 지도 초기화
        function initMap() {
            var container = document.getElementById('map');
            var options = { 
                center: new kakao.maps.LatLng(centerLat, centerLng),
                level: 3
            };
            var map = new kakao.maps.Map(container, options);

            var markerPosition  = new kakao.maps.LatLng(centerLat, centerLng); 
            var marker = new kakao.maps.Marker({
                position: markerPosition
            });
            marker.setMap(map);
        }   

        // 카카오맵 API 비동기 로드
        function loadScript() {
            var script = document.createElement('script');
            script.src = 'https://dapi.kakao.com/v2/maps/sdk.js?appkey=0d9764d3d7fd5c1dd0af3f9d719674e2&autoload=false';
            script.onload = function() {
                kakao.maps.load(initMap); // 지도 API를 로드한 후 initMap 함수 호출
            };
            document.head.appendChild(script);
        }

        document.addEventListener('DOMContentLoaded', loadScript);
        
        
    //pagination 설정 코드
    const totalPages = 6; // 총 페이지 수 설정
    const pageNumbersContainer = document.getElementById('page-numbers');
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');
    let currentPage = 1;

    // 페이지 번호 생성
    function createPageNumbers() {
        pageNumbersContainer.innerHTML = ''; // 기존 페이지 번호 삭제

        // 첫 페이지와 마지막 페이지 버튼 추가
        if (totalPages > 1) {
            for (let i = 1; i <= totalPages; i++) {
                const pageButton = document.createElement('button');
                pageButton.classList.add('page-number');
                pageButton.textContent = i;
                pageButton.addEventListener('click', function() {
                    currentPage = i;
                    updatePagination();
                });
                pageNumbersContainer.appendChild(pageButton);
            }
        }

        updatePagination();
    }

    // 페이지네이션 업데이트
    function updatePagination() {
        // 모든 페이지 번호 비활성화
        const pageNumbers = document.querySelectorAll('.page-number');
        pageNumbers.forEach(page => {
            page.classList.remove('active');
            if (parseInt(page.textContent) === currentPage) {
                page.classList.add('active');
            }
        });

        // 이전/다음 버튼 활성화/비활성화
        prevButton.disabled = currentPage === 1;
        nextButton.disabled = currentPage === totalPages;
    }

    // 이전 버튼 클릭 시
    prevButton.addEventListener('click', function() {
        if (currentPage > 1) {
            currentPage--;
            updatePagination();
        }
    });

    // 다음 버튼 클릭 시
    nextButton.addEventListener('click', function() {
        if (currentPage < totalPages) {
            currentPage++;
            updatePagination();
        }
    });

    // 초기 페이지네이션 설정
    createPageNumbers();
