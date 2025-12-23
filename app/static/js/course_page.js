document.addEventListener('DOMContentLoaded', () => {
    // Заполняем прогресс
    const completedModules = Number(document.getElementById('modules-progress-fill').dataset.completed);
    const totalModules = Number(document.getElementById('modules-progress-fill').dataset.total);
    const progressFill = document.getElementById('modules-progress-fill');

    if (totalModules > 0) {
        const percent = (completedModules / totalModules) * 100;
        progressFill.style.width = percent + '%';
    }

    // Переключение модулей
    const moduleItems = document.querySelectorAll('.module-item');
    const moduleDetails = document.querySelectorAll('.module-detail');

    moduleItems.forEach(item => {
        item.addEventListener('click', () => {
            const id = item.dataset.moduleId;

            moduleItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');

            moduleDetails.forEach(detail => {
                if (detail.dataset.moduleId === id) {
                    detail.classList.remove('hidden');
                } else {
                    detail.classList.add('hidden');
                }
            });
        });
    });
});
