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

document.querySelectorAll('.test-wrapper').forEach(testWrapper => {
    const questions = testWrapper.querySelectorAll('.question');
    const resultBlock = testWrapper.querySelector('.test-result');
    let currentIndex = 0;

    questions.forEach((q, index) => {
        const btnNext = q.querySelector('.btn-next-question');
        btnNext.addEventListener('click', () => {
            // Проверяем выбранный ответ
            const selected = q.querySelector('input[type="radio"]:checked');
            if (!selected) {
                alert('Выберите ответ перед переходом');
                return;
            }
            // Сохраняем правильность (можно массив, если нужен детальный анализ)
            if (!q.dataset.correctAnswers) q.dataset.correctAnswers = 0;
            if (selected.value === "True") {
                q.dataset.correctAnswers = 1;
            }

            // Скрываем текущий вопрос
            q.style.display = 'none';
            currentIndex++;

            if (currentIndex < questions.length) {
                // Показываем следующий вопрос
                questions[currentIndex].style.display = 'block';
            } else {
                // Последний вопрос -> показываем результат
                let correctCount = 0;
                questions.forEach(quest => {
                    correctCount += parseInt(quest.dataset.correctAnswers || 0);
                });
                const percent = Math.round((correctCount / questions.length) * 100);
                const resultText = percent >= 70 ?
                    `Тест пройден! Ваш результат: ${percent}%` :
                    `Попробуйте еще раз. Ваш результат: ${percent}%`;
                resultBlock.querySelector('.result-text').textContent = resultText;
                resultBlock.style.display = 'block';
            }
        });
    });

    // Кнопка "Попробовать еще раз"
    const btnRetry = resultBlock.querySelector('.btn-retry');
    btnRetry.addEventListener('click', () => {
        currentIndex = 0;
        resultBlock.style.display = 'none';
        questions.forEach((q, index) => {
            q.style.display = index === 0 ? 'block' : 'none';
            q.dataset.correctAnswers = 0;
            const radios = q.querySelectorAll('input[type="radio"]');
            radios.forEach(r => r.checked = false);
        });
    });
});

