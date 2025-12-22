document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.tab-content');
    const activeLine = document.querySelector('.active-line');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Снимаем active со всех вкладок и контента
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));

            // Активируем текущую вкладку и контент
            tab.classList.add('active');
            const tabName = tab.dataset.tab;
            document.getElementById(tabName + '-content').classList.add('active');

            // Линия под активной вкладкой
            activeLine.style.width = tab.offsetWidth + 'px';
            activeLine.style.left = tab.offsetLeft + 'px';
        });
    });

    // Линия под первой вкладкой при загрузке
    const initialTab = document.querySelector('.tab.active');
    activeLine.style.width = initialTab.offsetWidth + 'px';
    activeLine.style.left = initialTab.offsetLeft + 'px';
});

document.addEventListener('DOMContentLoaded', () => {
    const reviewCards = document.querySelectorAll('.review-card');

    reviewCards.forEach(card => {
        const rating = parseInt(card.dataset.rating); // фактический рейтинг
        const stars = card.querySelectorAll('.review-rating .star');

        // Инициализация: подсветка звезд согласно рейтингу
        stars.forEach((star, index) => {
            star.src = index < rating
                ? star.dataset.yellow || '/static/icons/star-yellow.svg'
                : star.dataset.gray || '/static/icons/star-gray.svg';
        });

        // Анимация при наведении
        stars.forEach((star, index) => {
            star.addEventListener('mouseenter', () => {
                stars.forEach((s, i) => {
                    s.src = i <= index
                        ? s.dataset.yellow || '/static/icons/star-yellow.svg'
                        : s.dataset.gray || '/static/icons/star-gray.svg';
                    s.style.transform = 'scale(1.2)';
                });
            });

            star.addEventListener('mouseleave', () => {
                stars.forEach((s, i) => {
                    s.src = i < rating
                        ? s.dataset.yellow || '/static/icons/star-yellow.svg'
                        : s.dataset.gray || '/static/icons/star-gray.svg';
                    s.style.transform = 'scale(1)';
                });
            });
        });
    });
});
