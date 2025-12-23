document.addEventListener('DOMContentLoaded', () => {
    // Вкладки
    const tabs = document.querySelectorAll('.tab-btn');
    const contents = document.querySelectorAll('#tab-content > div');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Снимаем активный класс со всех вкладок
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            // Показываем соответствующий контент
            const target = tab.dataset.tab;
            contents.forEach(c => {
                c.style.display = (c.classList.contains(target)) ? 'block' : 'none';
            });
        });
    });

    // Обновление прогресса на каждой карточке
    const courseCards = document.querySelectorAll('.course-card');
    courseCards.forEach(card => {
        const completedModules = parseInt(card.dataset.completedModules || 0);
        const totalModules = parseInt(card.dataset.totalModules || 0);
        const progressFill = card.querySelector('.progress-fill');
        const progressPercent = card.querySelector('.progress-percent');

        // Вычисляем процент прогресса
        let progress = 0;
        if (totalModules > 0) {
            progress = Math.round((completedModules / totalModules) * 100);
        }

        // Устанавливаем ширину и текст
        if (progressFill) progressFill.style.width = `${progress}%`;
        if (progressPercent) progressPercent.textContent = `${progress}%`;
    });
});
