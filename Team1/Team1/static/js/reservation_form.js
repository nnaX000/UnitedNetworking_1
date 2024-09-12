document.addEventListener("DOMContentLoaded", function() {
    var modal = document.getElementById("reservation-modal");
    var span = document.getElementsByClassName("close-btn")[0];
    
    // URL의 쿼리 파라미터를 확인하여 모달을 열기
    if (window.location.search.includes('reservation_success=true')) {
        modal.style.display = "block";
    }

    // 모달을 닫기
    span.onclick = function() {
        modal.style.display = "none";
    }

    // 모달 외부 클릭 시 닫기
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});
