document.addEventListener('DOMContentLoaded', () => {
    const courseId = document.querySelector('.course-page').dataset.courseId;

    const progressFill = document.getElementById('modules-progress-fill');
    const totalModules = Number(progressFill.dataset.total);
    let completedModules = Number(progressFill.dataset.completed);

    if (totalModules > 0) {
        progressFill.style.width = (completedModules / totalModules) * 100 + '%';
        progressFill.textContent = `${completedModules}/${totalModules}`;
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
                if(detail.dataset.moduleId === id){
                    detail.classList.remove('hidden');
                } else {
                    detail.classList.add('hidden');
                }
            });
        });
    });

    // Практика: кнопки "Продолжить" и "Отметить как выполнено"
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
            markModuleCompleted(moduleDiv.dataset.moduleId);
            e.target.disabled = true;
            e.target.textContent = 'Выполнено';
        }
    });

    // Тесты
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
                    questions.forEach(quest => { correctCount += parseInt(quest.dataset.correctAnswers || 0); });
                    const percent = Math.round((correctCount / questions.length) * 100);

                    if (percent >= 70) {
                        const moduleDiv = testWrapper.closest('.module-detail');
                        markModuleCompleted(moduleDiv.dataset.moduleId);
                    }

                    resultBlock.querySelector('.result-text').textContent =
                        percent >= 70 ? `Тест пройден! Ваш результат: ${percent}%` : `Попробуйте еще раз. Ваш результат: ${percent}%`;
                    resultBlock.style.display = 'block';
                }
            });
        });

        resultBlock.querySelector('.btn-retry').addEventListener('click', () => {
            currentIndex = 0;
            resultBlock.style.display = 'none';
            questions.forEach((q, i) => {
                q.style.display = i === 0 ? 'block' : 'none';
                q.dataset.correctAnswers = 0;
                q.querySelectorAll('input[type="radio"]').forEach(r => r.checked = false);
            });
        });
    });

    // Теория
    document.querySelectorAll('.theory-video-wrapper video').forEach(video => {
        video.addEventListener('ended', () => {
            const moduleDiv = video.closest('.module-detail');
            markModuleCompleted(moduleDiv.dataset.moduleId);
        });
    });

    function markModuleCompleted(moduleId) {
    const courseId = document.querySelector('.course-page').dataset.courseId;

    fetch(`/course/${courseId}/complete_module/${moduleId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            // Обновляем прогресс-бар
            const progressFill = document.getElementById('modules-progress-fill');
            if (progressFill) {
                const totalModules = Number(progressFill.dataset.total);
                const completed = data.completed_modules;
                const percent = Math.round((completed / totalModules) * 100);
                progressFill.style.width = percent + '%';
                progressFill.textContent = `${completed}/${totalModules}`;
            }

            // Отмечаем модуль как выполненный визуально
            const moduleItem = document.querySelector(`.module-item[data-module-id='${moduleId}']`);
            if(moduleItem) moduleItem.classList.add('completed');
        }
    })
    .catch(err => console.error(err));
}

});
