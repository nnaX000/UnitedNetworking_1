// 모든 별들에 클릭 이벤트 추가
const stars = document.querySelectorAll('.reviewEmptyStar-icon');
let currentRating = 0; // 현재 채워진 별 개수

stars.forEach(star => {
    star.addEventListener('click', () => {
        const starValue = parseInt(star.getAttribute('data-value'));

        if (starValue <= currentRating) {
            // 다시 누른 경우 -> 빈 별로 되돌리기
            fillStars(starValue - 1);
        } else {
            // 왼쪽에서 오른쪽으로 별 채우기
            fillStars(starValue);
        }
    });
});

function fillStars(rating) {
    currentRating = rating;
    stars.forEach(star => {
        const starValue = parseInt(star.getAttribute('data-value'));
        if (starValue <= currentRating) {
            star.classList.add('filled'); // 별을 채움
        } else {
            star.classList.remove('filled'); // 빈 별로 바꿈
        }
    });
}


document.querySelectorAll('.keyword-button').forEach(button => {
    button.addEventListener('click', () => {
        button.classList.toggle('selected');
    });
});

//글자수 세기 기능
document.addEventListener('DOMContentLoaded', () => {
    const textarea = document.getElementById('textInput');
    const charCount = document.getElementById('charCount');

    textarea.addEventListener('input', () => {
        const currentLength = textarea.value.length;
        charCount.textContent = `${currentLength}/50`;
    });
});
