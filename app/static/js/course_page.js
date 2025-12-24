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

document.addEventListener('click', function (e) {
    if (!e.target.classList.contains('btn-next-stage')) return;

    const currentStage = e.target.closest('.practice-stage');
    const nextStage = currentStage.nextElementSibling;

    // скрываем кнопку "Продолжить" у текущего этапа
    e.target.remove();

    // показываем следующий этап
    if (nextStage && nextStage.classList.contains('practice-stage')) {
        nextStage.classList.remove('hidden');
        nextStage.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
});
