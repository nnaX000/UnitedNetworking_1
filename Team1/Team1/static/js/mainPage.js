// 페이지가 처음 로드될 때 데이터를 가져옵니다.
document.addEventListener('DOMContentLoaded', function() {
    fetch(`/mainPage/filter_centers/`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = ''; 

            if (data.length > 0) {
                data.forEach(center => {
                    const resultItem = document.createElement('div');
                    resultItem.classList.add('result-item');
                    resultItem.innerHTML = `
                        <h3>${center['센터 이름']}</h3>
                        <img src="${center['사진']}" alt="${center['센터 이름']} 사진">
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
                    <h3>${center['센터 이름']}</h3>
                    <img src="${center['사진']}" alt="${center['센터 이름']} 사진">
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