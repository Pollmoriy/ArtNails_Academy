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
