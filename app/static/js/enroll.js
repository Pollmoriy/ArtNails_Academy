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
