// Ad rotation logic
let currentAdIndex = 0;
const ads = document.querySelectorAll('.ad');
const totalAds = ads.length;

function showNextAd() {
    ads.forEach((ad, index) => {
        ad.style.display = 'none'; // Hide all ads
    });

    ads[currentAdIndex].style.display = 'block'; // Show the current ad
    currentAdIndex = (currentAdIndex + 1) % totalAds; // Move to the next ad
}

setInterval(showNextAd, 3000); // Rotate ads every 3 seconds

document.querySelector('.chatbot-box').addEventListener('click', function() {
    window.location.href = 'chatbot.html'; // Redirect to the chatbot page
});

// 페이지가 처음 로드될 때 데이터를 가져옵니다.
document.addEventListener('DOMContentLoaded', function() {
    fetch(`/mainPage/filter_centers/`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = ''; 

            if (data.length > 0) {
                data.slice(0, 3).forEach(center => {
                    const resultItem = document.createElement('div');
                    resultItem.classList.add('result-item');
                    resultItem.innerHTML = `
                        <div class="result-item-inner">
                            <div class="result-image-container">
                                <img src="${center['사진']}" alt="${center['센터 이름']} 사진" class="result-image">
                            </div>
                            <div class="result-info-container">
                                <h3 class="result-name">${center['센터 이름']}</h3>
                                <p class="result-address">${center['주소']}</p>
                            </div>
                        </div>
                    `;
                    resultItem.addEventListener('click', function() {
                        window.location.href = `center/${center['id']}/`;
                    });
                    resultsDiv.appendChild(resultItem);
                });
            } else {
                resultsDiv.innerHTML = '<p>검색 결과가 없습니다.</p>';
            }
        });
});


document.getElementById('searchButton').addEventListener('click', function() {
const dong = document.getElementById('dong').value;
const exercise = document.getElementById('exercise').value;

fetch(`/mainPage/filter_centers/?dong=${dong}&exercise=${exercise}`)
    .then(response => response.json())
    .then(data => {
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = ''; 

        if (data.length > 0) {
            data.forEach(center => {
                const resultItem = document.createElement('div');
                resultItem.classList.add('result-item');
                resultItem.innerHTML = `
                    <div class="result-item-inner">
                        <div class="result-image-container">
                            <img src="${center['사진']}" alt="${center['센터 이름']} 사진" class="result-image">
                        </div>
                        <div class="result-info-container">
                            <h3 class="result-name">${center['센터 이름']}</h3>
                        </div>
                    </div>
                `;
                resultItem.addEventListener('click', function() {
                    window.location.href = `center/${center['id']}/`;
                });
                resultsDiv.appendChild(resultItem);
            });
        } else {
            resultsDiv.innerHTML = '<p>검색 결과가 없습니다.</p>';
        }
    });
});