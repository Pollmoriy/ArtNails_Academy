document.addEventListener('DOMContentLoaded', () => {

    const form = document.getElementById('enrollForm');
    const courseSelect = document.getElementById('courseSelect');
    const summaryContent = document.getElementById('summaryContent');

    courseSelect.addEventListener('change', () => {
        const selectedOption = courseSelect.options[courseSelect.selectedIndex];

        if (!selectedOption.value) {
            summaryContent.innerHTML = `
                <p class="summary-placeholder">
                    Выберите курс для отображения информации
                </p>
            `;
            return;
        }

        const title = selectedOption.text;
        const price = selectedOption.dataset.price;

        summaryContent.innerHTML = `
            <p><strong>Курс:</strong> ${title}</p>
            <p><strong>Цена:</strong> ${price} BYN</p>
        `;
    });

    // ---------- SUBMIT ----------
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const courseId = courseSelect.value;
        if (!courseId) {
            alert('Выберите курс');
            return;
        }

        try {
            const response = await fetch('/enroll/create-stripe-session', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    course_id: courseId
                })
            });

            if (!response.ok) {
                throw new Error('Ошибка сервера');
            }

            const data = await response.json();
            window.location.href = data.url;

        } catch (err) {
            alert('Ошибка при переходе к оплате');
            console.error(err);
        }
    });

});
