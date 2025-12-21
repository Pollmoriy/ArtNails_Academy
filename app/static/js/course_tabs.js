document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.tab-content');
    const activeLine = document.querySelector('.active-line');

    function updateLine(tab) {
        activeLine.style.left = tab.offsetLeft + 'px';
        activeLine.style.width = tab.offsetWidth + 'px';
    }

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            contents.forEach(c => c.classList.remove('active'));
            const content = document.getElementById(`${tab.dataset.tab}-content`);
            if (content) content.classList.add('active');

            updateLine(tab);
        });
    });

    const initialTab = document.querySelector('.tab.active');
    if (initialTab) updateLine(initialTab);

    window.addEventListener('resize', () => {
        const currentTab = document.querySelector('.tab.active');
        if (currentTab) updateLine(currentTab);
    });
});
