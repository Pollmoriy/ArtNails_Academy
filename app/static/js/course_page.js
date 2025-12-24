document.addEventListener('DOMContentLoaded', () => {
    const coursePage = document.querySelector('.course-page');
    if (!coursePage) return;

    const courseId = coursePage.dataset.courseId;

    // --- Элементы прогресса ---
    const progressFill = document.getElementById('modules-progress-fill');
    const progressText = document.querySelector('.progress-text');

    let completedModules = Number(progressFill.dataset.completed) || 0;
    let totalModules = Number(progressFill.dataset.total) || 0;

    function updateProgress(completed) {
        completedModules = completed;
        const percent = totalModules > 0 ? Math.round((completedModules / totalModules) * 100) : 0;
        progressFill.style.width = percent + '%';
        progressText.textContent = `${completedModules}/${totalModules}`;
    }

    // Инициализация прогресса при загрузке
    updateProgress(completedModules);

    // --- Переключение модулей ---
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

    // --- Отметка модуля как выполненного ---
    function markModuleCompleted(moduleId) {
        fetch(`/course/${courseId}/complete_module/${moduleId}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                const moduleItem = document.querySelector(`.module-item[data-module-id="${moduleId}"]`);
                if (moduleItem) moduleItem.classList.add('completed');
                updateProgress(data.completed_modules);
            }
        })
        .catch(err => console.error(err));
    }

    // --- Видео ---
    document.querySelectorAll('.theory-video-wrapper video').forEach(video => {
        video.addEventListener('ended', () => {
            const moduleDiv = video.closest('.module-detail');
            if (!moduleDiv) return;
            const moduleId = moduleDiv.dataset.moduleId;
            markModuleCompleted(moduleId);
        });
    });

    // --- Практика ---
    document.addEventListener('click', e => {
        // Кнопка перехода к следующему этапу
        if (e.target.classList.contains('btn-next-stage')) {
            const currentStage = e.target.closest('.practice-stage');
            const nextStage = currentStage?.nextElementSibling;
            e.target.remove();
            if (nextStage && nextStage.classList.contains('practice-stage')) {
                nextStage.classList.remove('hidden');
                nextStage.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }

        // Кнопка отметить модуль выполненным
        if (e.target.classList.contains('btn-mark-completed')) {
            const moduleDiv = e.target.closest('.module-detail');
            if (!moduleDiv) return;
            const moduleId = moduleDiv.dataset.moduleId;
            markModuleCompleted(moduleId);
            e.target.disabled = true;
            e.target.textContent = 'Выполнено';
        }
    });

    // --- Тесты ---
    document.querySelectorAll('.test-wrapper').forEach(testWrapper => {
        const questions = testWrapper.querySelectorAll('.question');
        const resultBlock = testWrapper.querySelector('.test-result');
        let currentIndex = 0;

        questions.forEach((q, index) => {
            const btnNext = q.querySelector('.btn-next-question');
            btnNext.addEventListener('click', () => {
                const selected = q.querySelector('input[type="radio"]:checked');
                if (!selected) {
                    alert('Выберите ответ');
                    return;
                }

                q.dataset.correctAnswers = selected.value === "True" ? 1 : 0;
                q.style.display = 'none';
                currentIndex++;

                if (currentIndex < questions.length) {
                    questions[currentIndex].style.display = 'block';
                } else {
                    let correctCount = 0;
                    questions.forEach(quest => {
                        correctCount += parseInt(quest.dataset.correctAnswers || 0);
                    });
                    const percent = Math.round((correctCount / questions.length) * 100);

                    // Если >=70%, отмечаем модуль завершённым
                    if (percent >= 70) {
                        const moduleId = testWrapper.closest('.module-detail')?.dataset.moduleId;
                        if (moduleId) markModuleCompleted(moduleId);
                    }

                    resultBlock.querySelector('.result-text').textContent =
                        percent >= 70 ?
                        `Тест пройден! Ваш результат: ${percent}%` :
                        `Попробуйте еще раз. Ваш результат: ${percent}%`;
                    resultBlock.style.display = 'block';
                }
            });
        });

        const btnRetry = resultBlock.querySelector('.btn-retry');
        btnRetry.addEventListener('click', () => {
            currentIndex = 0;
            resultBlock.style.display = 'none';
            questions.forEach((q, idx) => {
                q.style.display = idx === 0 ? 'block' : 'none';
                q.dataset.correctAnswers = 0;
                q.querySelectorAll('input[type="radio"]').forEach(r => r.checked = false);
            });
        });
    });
});
