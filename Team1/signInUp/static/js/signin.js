
// 백엔드에서 닉네임 데이터를 받아와서 표시
document.getElementById('nickname').textContent = '{{ request.POST.nickname }}';

// 로그인 버튼 클릭 시 login.html로 이동
document.getElementById('loginButton').addEventListener('click', function() {
    window.location.href = 'login.html';
});