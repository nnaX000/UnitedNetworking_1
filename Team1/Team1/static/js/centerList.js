const itemsPerPage = 3; // 한 페이지에 보여줄 센터 수
let centers = []; // CSV 데이터에서 가져온 센터 데이터 배열
let totalPages = 1; // 페이지 수 초기화

// 페이지에 맞는 데이터를 렌더링하는 함수
function renderCenters(page) {
    const listContainer = document.querySelector('.listContainer');
    listContainer.innerHTML = ''; // 이전 데이터를 제거

    const start = (page - 1) * itemsPerPage;
    const end = start + itemsPerPage;

    // centers 배열에서 현재 페이지에 맞는 데이터 가져오기
    const centersToShow = centers.slice(start, end); 
    centersToShow.forEach(center => {
        const boxContainer = document.createElement('div');
        boxContainer.classList.add('boxContainer');
        boxContainer.innerHTML = `
            <img src="${center.image_url}" alt="센터 사진" class="centerImage">
            <div class="centerContent">
                <div class="title-content">
                    <p class="titleContent-centerName">${center.name}</p>
                    <img src="/Team1/Team1/static/img/reviewStar-icon.png" alt="리뷰 별 점수" class="reviewStar-icon">
                    <p class="titleContent-score">5.0</p>
                </div>
                <div class="centerDetail-container">
                    <p class="centerDetail-address">${center.address}</p>
                    <p class="centerDetail-phone">${center.phone}</p>
                </div>
            </div>
        `;
        listContainer.appendChild(boxContainer);
    });
}

// 페이지 번호 생성 함수
function createPageNumbers() {
    pageNumbersContainer.innerHTML = ''; // 기존 페이지 번호 삭제

    // 페이지 수 계산
    totalPages = Math.ceil(centers.length / itemsPerPage);

    // 페이지 번호 버튼 생성
    if (totalPages > 1) {
        for (let i = 1; i <= totalPages; i++) {
            const pageButton = document.createElement('button');
            pageButton.classList.add('page-number');
            pageButton.textContent = i;
            pageButton.addEventListener('click', function () {
                currentPage = i;
                updatePagination();
                renderCenters(currentPage); // 페이지 번호 클릭 시 센터 렌더링
            });
            pageNumbersContainer.appendChild(pageButton);
        }
    }

    updatePagination();
    renderCenters(currentPage); // 첫 페이지 렌더링
}

// 페이지네이션 업데이트 함수
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
prevButton.addEventListener('click', function () {
    if (currentPage > 1) {
        currentPage--;
        updatePagination();
        renderCenters(currentPage); // 이전 페이지로 이동 시 센터 렌더링
    }
});

// 다음 버튼 클릭 시
nextButton.addEventListener('click', function () {
    if (currentPage < totalPages) {
        currentPage++;
        updatePagination();
        renderCenters(currentPage); // 다음 페이지로 이동 시 센터 렌더링
    }
});

// CSV 데이터 로드 후 페이지네이션 설정
function loadData() {
    // 예를 들어, CSV 데이터를 로드하여 centers 배열에 저장하는 코드
    // centers = [ { image_url: '...', name: '...', address: '...', phone: '...' }, ... ];

    // 데이터 로드 후 페이지네이션 설정
    createPageNumbers();
}

// 데이터 로드 호출
loadData();
