document.addEventListener('DOMContentLoaded', () => {
    const courseId = document.querySelector('.course-page').dataset.courseId;

    // --- Прогресс-бар ---
    const progressFill = document.getElementById('modules-progress-fill');
    const totalModules = Number(progressFill.dataset.total);

    function updateProgress(completed) {
        const percent = Math.round((completed / totalModules) * 100);
        progressFill.style.width = percent + '%';
        document.querySelector('.progress-text').textContent = `${completed}/${totalModules}`;
    }

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

    // --- Функция отметки модуля как выполненного ---
    function markModuleCompleted(moduleId) {
        fetch(`/course/${courseId}/complete_module/${moduleId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                // Отметить модуль на фронте зеленым
                const moduleItem = document.querySelector(`.module-item[data-module-id="${moduleId}"]`);
                if (moduleItem) moduleItem.classList.add('completed');

                // Обновить прогресс
                updateProgress(data.completed_modules);
            }
        })
        .catch(err => console.error(err));
    }

    // --- Видео ---
    document.querySelectorAll('.theory-video-wrapper video').forEach(video => {
        video.addEventListener('ended', () => {
            const moduleDiv = video.closest('.module-detail');
            const moduleId = moduleDiv.dataset.moduleId;
            markModuleCompleted(moduleId);
        });
    });

    // --- Практика ---
    document.addEventListener('click', e => {
        if (e.target.classList.contains('btn-next-stage')) {
            const currentStage = e.target.closest('.practice-stage');
            const nextStage = currentStage.nextElementSibling;
            e.target.remove();

            if (nextStage && nextStage.classList.contains('practice-stage')) {
                nextStage.classList.remove('hidden');
                nextStage.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }

        if (e.target.classList.contains('btn-mark-completed')) {
            const moduleDiv = e.target.closest('.module-detail');
            const moduleId = moduleDiv.dataset.moduleId;
            markModuleCompleted(moduleId);
            e.target.disabled = true;
            e.target.textContent = 'Выполнено';
        }
    });

    // --- Тест ---
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

                    if (percent >= 70) {
                        const moduleId = testWrapper.closest('.module-detail').dataset.moduleId;
                        markModuleCompleted(moduleId);
                    }

                    resultBlock.querySelector('.result-text').textContent =
                        percent >= 70 ? `Тест пройден! Ваш результат: ${percent}%` :
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

const completedModules = Number(document.getElementById('modules-progress-fill').dataset.completed);
const totalModules = Number(document.getElementById('modules-progress-fill').dataset.total);
const progressFill = document.getElementById('modules-progress-fill');

if (totalModules > 0) {
    const percent = (completedModules / totalModules) * 100;
    progressFill.style.width = percent + '%';
    progressFill.textContent = `${completedModules}/${totalModules}`;
}
