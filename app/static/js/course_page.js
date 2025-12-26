document.addEventListener('DOMContentLoaded', () => {

    const coursePage = document.querySelector('.course-page');
    if (!coursePage) return;

    /* ===================== */
    /* ПЕРВАЯ ЗАГРУЗКА */
    /* ===================== */

    setTimeout(() => {
        coursePage.classList.add('page-loaded');
        document.querySelector('.modules-list')?.classList.add('visible');
        document.querySelector('.module-content')?.classList.add('visible');
    }, 100);

    const courseId = coursePage.dataset.courseId;

    /* ===================== */
    /* ПРОГРЕСС */
    /* ===================== */

    const progressFill = document.getElementById('modules-progress-fill');
    const progressText = document.querySelector('.progress-text');

    let completedModules = Number(progressFill.dataset.completed) || 0;
    let totalModules = Number(progressFill.dataset.total) || 0;

    function updateProgress(value) {
        const percent = totalModules
            ? Math.round((value / totalModules) * 100)
            : 0;

        requestAnimationFrame(() => {
            progressFill.style.width = percent + '%';
            progressText.textContent = `${value}/${totalModules}`;
        });
    }

    setTimeout(() => updateProgress(completedModules), 300);

    /* ===================== */
    /* ПЕРЕКЛЮЧЕНИЕ МОДУЛЕЙ */
    /* ===================== */

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

    /* ===================== */
    /* ОТМЕТКА МОДУЛЯ */
    /* ===================== */

    function markModuleCompleted(moduleId) {
        fetch(`/course/${courseId}/complete_module/${moduleId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                document
                    .querySelector(`.module-item[data-module-id="${moduleId}"]`)
                    ?.classList.add('completed');

                updateProgress(data.completed_modules);
            }
        });
    }

    /* ===================== */
    /* ВИДЕО */
    /* ===================== */

    document.querySelectorAll('video').forEach(video => {
        video.addEventListener('ended', () => {
            const moduleId = video.closest('.module-detail')?.dataset.moduleId;
            if (moduleId) markModuleCompleted(moduleId);
        });
    });

    /* ===================== */
    /* ПРАКТИКА */
    /* ===================== */

    document.addEventListener('click', e => {

        if (e.target.classList.contains('btn-next-stage')) {
            const current = e.target.closest('.practice-stage');
            const next = current.nextElementSibling;

            e.target.remove();

            if (next) {
                next.classList.remove('hidden');
                next.scrollIntoView({ behavior: 'smooth' });
            }
        }

        if (e.target.classList.contains('btn-mark-completed')) {
            const moduleId = e.target.closest('.module-detail')?.dataset.moduleId;
            if (!moduleId) return;

            markModuleCompleted(moduleId);
            e.target.textContent = 'Выполнено';
            e.target.disabled = true;
        }
    });

    /* ===================== */
    /* ТЕСТЫ */
    /* ===================== */

    document.querySelectorAll('.test-wrapper').forEach(wrapper => {
        const questions = wrapper.querySelectorAll('.question');
        const result = wrapper.querySelector('.test-result');
        let index = 0;

        questions.forEach((q, i) => {
            q.querySelector('.btn-next-question').addEventListener('click', () => {
                const checked = q.querySelector('input:checked');
                if (!checked) return alert('Выберите ответ');

                q.dataset.correct = checked.value === 'True' ? 1 : 0;
                q.style.display = 'none';
                index++;

                if (questions[index]) {
                    questions[index].style.display = 'block';
                } else {
                    let score = 0;
                    questions.forEach(x => score += Number(x.dataset.correct || 0));
                    const percent = Math.round(score / questions.length * 100);

                    if (percent >= 70) {
                        const moduleId = wrapper.closest('.module-detail')?.dataset.moduleId;
                        if (moduleId) markModuleCompleted(moduleId);
                    }

                    result.style.display = 'block';
                    result.querySelector('.result-text').textContent =
                        percent >= 70
                            ? `Тест пройден! ${percent}%`
                            : `Попробуйте снова. ${percent}%`;
                }
            });
        });

        result.querySelector('.btn-retry').addEventListener('click', () => {
            index = 0;
            result.style.display = 'none';

            questions.forEach((q, i) => {
                q.style.display = i === 0 ? 'block' : 'none';
                q.dataset.correct = 0;
                q.querySelectorAll('input').forEach(r => r.checked = false);
            });
        });
    });
});
