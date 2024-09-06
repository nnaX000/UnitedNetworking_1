document.addEventListener('DOMContentLoaded', function() {
    // 서버에서 `logged_in` 상태를 포함한 데이터를 가져온다고 가정합니다
    fetch('/get-login-status') // 이 URL은 서버에서 로그인 상태를 반환하는 엔드포인트입니다.
        .then(response => response.json())
        .then(data => {
            if (!data.logged_in) {
                const purchaseButtons = document.querySelectorAll('.purchase-button');
                purchaseButtons.forEach(button => {
                    button.disabled = true;
                });
            }
        })
        .catch(error => {
            console.error('Error fetching login status:', error);
        });
});
