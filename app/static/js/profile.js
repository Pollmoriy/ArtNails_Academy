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
});

