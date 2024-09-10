function goBack() {
    window.history.back(); // Navigate to the previous page
}

function validateForm() {
    let isValid = true;

    // Email validation
    const email = document.getElementById("email").value;
    const emailError = document.getElementById("email-error");
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        emailError.textContent = "이메일 주소를 다시 확인해주세요.";
        emailError.style.display = "block";
        isValid = false;
    } else {
        emailError.style.display = "none";
    }

    // Password validation
    const password = document.getElementById("password").value;
    const passwordError = document.getElementById("password-error");
    const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    if (!passwordRegex.test(password)) {
        passwordError.textContent = "비밀번호는 문자/숫자/기호를 사용하여 8자리 이상이여야합니다.";
        passwordError.style.display = "block";
        isValid = false;
    } else {
        passwordError.style.display = "none";
    }

    // Confirm password validation
    const confirmPassword = document.getElementById("repeated_password").value;
    const confirmPasswordError = document.getElementById("repeated-password-error");
    if (password !== confirmPassword) {
        confirmPasswordError.textContent = "비밀번호가 일치하지 않습니다.";
        confirmPasswordError.style.display = "block";
        isValid = false;
    } else {
        confirmPasswordError.style.display = "none";
    }

    // Nickname validation
    const nickname = document.getElementById("nickname").value;
    const nicknameError = document.getElementById("nickname-error");
    if (nickname.length < 1 || nickname.length > 8) {
        nicknameError.textContent = "닉네임은 8자 이내여야합니다.";
        nicknameError.style.display = "block";
        isValid = false;
    } else {
        nicknameError.style.display = "none";
    }

    // Gender validation
    const gender = document.getElementById("gender").value;
    const genderError = document.getElementById("gender-error");
    if (!gender) {
        genderError.textContent = "성별을 선택해주세요.";
        genderError.style.display = "block";
        isValid = false;
    } else {
        genderError.style.display = "none";
    }

    //birthday validation
    document.getElementById("submit").addEventListener("click", function() {
        const birthYear = document.getElementById("birth_year").value;
        const birthMonth = document.getElementById("birth_month").value;
        const birthDay = document.getElementById("birth_day").value;
        const birthError = document.getElementById("birth-error");
    
        if (!birthYear || !birthMonth || !birthDay) {
            birthError.textContent = "생년월일을 입력해주세요.";
            birthError.style.display = "block";
            isValid = false;
        } else {
            birthError.style.display = "none";
        }
    });
    

    // Privacy agreement validation
    const privacyAgree = document.querySelector('input[name="privacy"]:checked');
    const privacyError = document.getElementById("privacy-error");
    if (!privacyAgree || privacyAgree.value === "disagree") {
        privacyError.textContent = "개인 정보 수집 및 이용에 동의해야 합니다.";
        privacyError.style.display = "block";
        isValid = false;
    } else {
        privacyError.style.display = "none";
    }

    // Final validation
    const submitError = document.getElementById("submit-error");
    if (!isValid) {
        submitError.textContent = "빠진 정보가 없는지 확인해주세요.";
        submitError.style.display = "block";
        return false; // Prevent form submission
    } else {
        submitError.style.display = "none";
        alert("가입이 완료되었습니다!");
        return true; // Allow form submission
    }
}

document.getElementById("male-btn").addEventListener("click", function () {
    // Set the value of the hidden gender input to "male"
    document.getElementById("gender").value = "male";
    // Apply the selected class to the male button and remove it from the female button
    document.getElementById("male-btn").classList.add("selected");
    document.getElementById("female-btn").classList.remove("selected");
});

document.getElementById("female-btn").addEventListener("click", function () {
    // Set the value of the hidden gender input to "female"
    document.getElementById("gender").value = "female";
    // Apply the selected class to the female button and remove it from the male button
    document.getElementById("female-btn").classList.add("selected");
    document.getElementById("male-btn").classList.remove("selected");
});
