// catalog_filter.js

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search');
    const levelSelect = document.getElementById('level');
    const priceSelect = document.getElementById('price');
    const durationSelect = document.getElementById('duration');
    const coursesContainer = document.getElementById('courses-container');

    // DEBUG: функция для логирования текущих параметров
    function debugParams(params) {
        console.log("DEBUG: Параметры фильтров", params);
    }

    function fetchCourses() {
        // Получаем значения фильтров
        let search = searchInput.value || '';
        let level = levelSelect.value || null;  // null вместо пустой строки
        let price = priceSelect.value || '';
        let duration = durationSelect.value || '';

        // Преобразуем price в диапазоны
        let price_min = 0, price_max = 999999;
        if (price === 'low') price_max = 800;
        else if (price === 'medium') { price_min = 801; price_max = 1200; }
        else if (price === 'high') price_min = 1201;

        // Преобразуем duration в диапазоны
        let duration_min = 0, duration_max = 100;
        if (duration === 'short') duration_max = 2;
        else if (duration === 'medium') { duration_min = 3; duration_max = 4; }
        else if (duration === 'long') duration_min = 5;

        // DEBUG: выводим все параметры
        debugParams({search, level, price_min, price_max, duration_min, duration_max});

        // AJAX запрос
        fetch(`/catalog?ajax=1&search=${encodeURIComponent(search)}&level=${encodeURIComponent(level || '')}&price_min=${price_min}&price_max=${price_max}&duration_min=${duration_min}&duration_max=${duration_max}`)
        .then(response => response.json())
        .then(data => {
            // DEBUG: выводим результат
            console.log("DEBUG: Полученные курсы", data);

            // Обновляем карточки
            coursesContainer.innerHTML = '';
            if (data.length === 0) {
                coursesContainer.innerHTML = '<p>Курсы не найдены.</p>';
                return;
            }

            data.forEach(course => {
                const card = document.createElement('div');
                card.classList.add('course-card');
                card.innerHTML = `
                    <img src="/static/${course.image}" alt="${course.title}" class="course-img">
                    <div class="course-top-info">
                        <span class="course-level">${course.difficulty}</span>
                        <span class="course-duration">${course.duration_weeks} недели</span>
                    </div>
                    <h3 class="course-name">${course.title}</h3>
                    <p class="course-desc">${course.short_description}</p>
                    <span class="course-price">${course.price} BYN</span>
                    <button class="btn-course-details">Подробнее</button>
                `;
                coursesContainer.appendChild(card);
            });
        })
        .catch(err => console.error("DEBUG: Ошибка при fetch", err));
    }

    // Вешаем обработчики событий
    searchInput.addEventListener('input', fetchCourses);
    levelSelect.addEventListener('change', fetchCourses);
    priceSelect.addEventListener('change', fetchCourses);
    durationSelect.addEventListener('change', fetchCourses);
});
