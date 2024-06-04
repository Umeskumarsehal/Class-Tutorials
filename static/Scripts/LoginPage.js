

// Function to handle radio button background color
function updateRadioLabelColors() {
    const studentRadio = document.getElementById('student');
    const teacherRadio = document.getElementById('teacher');
    const studentLabel = document.getElementById('student_label');
    const teacherLabel = document.getElementById('teacher_label');
    const emailField = document.getElementById('email_field');
    

    if (studentRadio.checked) {
        studentLabel.style.backgroundColor = 'var(--button-color)';
        studentLabel.style.color = 'var(--white)';
        teacherLabel.style.backgroundColor = 'transparent';
        teacherLabel.style.color = 'var(--bg-color2)';
    } else if (teacherRadio.checked) {
        studentLabel.style.backgroundColor = 'transparent';
        studentLabel.style.color = 'var(--bg-color2)';
        teacherLabel.style.backgroundColor = 'var(--button-color)';
        teacherLabel.style.color = 'var(--white)';
    }
}

// Handle form submission
document.getElementById('login-form').addEventListener('submit', function (event) {
    let isValid = false;

    isValid = checkValidEmail();
    isValid = checkValidPassword();

    if (!isValid) {
        event.preventDefault();
    }
});


// Event listeners for radio buttons
document.getElementById('student').addEventListener('change', updateRadioLabelColors);
document.getElementById('teacher').addEventListener('change', updateRadioLabelColors);

// Initial call to set the correct colors
updateRadioLabelColors();