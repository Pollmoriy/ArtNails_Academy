document.addEventListener('DOMContentLoaded', () => {
    const courseSelect = document.querySelector('.enroll-form select');
    const summaryBlock = document.querySelector('.order-summary');

    courseSelect.addEventListener('change', () => {
        const selectedCourse = courseSelect.value;

        summaryBlock.innerHTML = `
            <h3 class="summary-title">Сводка заказа</h3>

            <div class="summary-item">
                <span class="summary-label">Курс:</span>
                <span class="summary-value">${selectedCourse}</span>
            </div>

            <div class="summary-item">
                <span class="summary-label">Стоимость:</span>
                <span class="summary-value">500 BYN</span>
            </div>

            <div class="order-guarantee">
                <strong>Гарантия качества</strong>
                <p>Возврат средств в течение 14 дней, если курс не подошёл</p>
            </div>
        `;
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('enrollForm');

    form.addEventListener('submit', (e) => {
        let valid = true;

        // очистка ошибок
        form.querySelectorAll('.error-text').forEach(el => el.textContent = '');
        form.querySelectorAll('.error').forEach(el => el.classList.remove('error'));

        // Имя
        const name = form.full_name;
        if (name.value.trim().length < 3) {
            showError(name, 'Введите имя и фамилию');
            valid = false;
        }

        // Email
        const email = form.email;
        if (!email.value.includes('@')) {
            showError(email, 'Введите корректный email');
            valid = false;
        }

        // Телефон
        const phone = form.phone;
        if (phone.value.trim().length < 7) {
            showError(phone, 'Введите номер телефона');
            valid = false;
        }

        // Курс
        const course = form.course;
        if (!course.value) {
            showError(course, 'Выберите курс');
            valid = false;
        }

        // Оплата
        const payment = form.querySelector('input[name="payment"]:checked');
        if (!payment) {
            showError(
                form.querySelector('.form-group:last-of-type'),
                'Выберите способ оплаты'
            );
            valid = false;
        }

        // Чекбокс
        const agree = form.querySelector('input[name="agree"]');
        if (!agree.checked) {
            showError(agree, 'Необходимо согласие с условиями');
            valid = false;
        }

        if (!valid) {
            e.preventDefault();
        }
    });

    function showError(element, message) {
        const container = element.closest('.form-group') || element.closest('.agreement');
        const error = container.querySelector('.error-text');
        if (error) error.textContent = message;
        element.classList.add('error');
    }
});
