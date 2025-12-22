document.addEventListener('DOMContentLoaded', () => {
    const courseSelect = document.getElementById('course');
    const summaryContent = document.getElementById('summaryContent');
    const payBtn = document.getElementById('payBtn');

    let selectedCourseId = null;

    courseSelect.addEventListener('change', () => {
        const selectedOption = courseSelect.options[courseSelect.selectedIndex];
        selectedCourseId = selectedOption.value;

        if (selectedCourseId) {
            const price = selectedOption.dataset.price;
            summaryContent.innerHTML = `
                <div class="summary-item">
                    <span class="summary-label">Курс:</span>
                    <span class="summary-value">${selectedOption.text}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-label">Стоимость:</span>
                    <span class="summary-value">${price} USD</span>
                </div>
            `;
        } else {
            summaryContent.innerHTML = `<p class="summary-placeholder">Выберите курс для отображения информации</p>`;
        }
    });

    payBtn.addEventListener('click', () => {
        if (!selectedCourseId) {
            alert('Выберите курс для оплаты!');
            return;
        }

        fetch('/enroll/create-stripe-session', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({course_id: selectedCourseId})
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                const stripeObj = Stripe('pk_test_ваш_публичный_ключ'); // вставь свой ключ
                stripeObj.redirectToCheckout({sessionId: data.id});
            }
        })
        .catch(err => console.error(err));
    });
});
