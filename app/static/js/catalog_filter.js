const searchInput = document.getElementById('search');
const levelSelect = document.getElementById('level');
const priceSelect = document.getElementById('price');
const durationSelect = document.getElementById('duration');
const container = document.getElementById('courses-container');
const suggestions = document.getElementById('search-suggestions');

let timeout = null;

function fetchCourses() {
    const params = new URLSearchParams({
        search: searchInput.value,
        level: levelSelect.value,
        price: priceSelect.value,
        duration: durationSelect.value
    });

    fetch(`/catalog?${params.toString()}`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(res => res.json())
    .then(data => {
        renderCourses(data);
        updateSuggestions(data);
    });
}

function renderCourses(courses) {
    container.innerHTML = '';

    if (courses.length === 0) {
        container.innerHTML = '<p>Курсы не найдены</p>';
        return;
    }

    courses.forEach(course => {
        const card = document.createElement('div');
        card.className = 'course-card';

        // Изображение
        const img = document.createElement('img');
        img.src = `/static/${course.image}`;
        img.alt = course.title;
        img.className = 'course-img';
        card.appendChild(img);

        // Верхняя информация
        const topInfo = document.createElement('div');
        topInfo.className = 'course-top-info';

        const levelSpan = document.createElement('span');
        levelSpan.className = 'course-level';
        levelSpan.textContent = course.difficulty;

        const durationSpan = document.createElement('span');
        durationSpan.className = 'course-duration';
        durationSpan.textContent = `${course.duration_weeks} недели`;

        topInfo.appendChild(levelSpan);
        topInfo.appendChild(durationSpan);
        card.appendChild(topInfo);

        // Название
        const title = document.createElement('h3');
        title.className = 'course-name';
        title.textContent = course.title;
        card.appendChild(title);

        // Описание
        const desc = document.createElement('p');
        desc.className = 'course-desc';
        desc.textContent = course.short_description;
        card.appendChild(desc);

        // Цена
        const price = document.createElement('span');
        price.className = 'course-price';
        price.textContent = `${course.price} BYN`;
        card.appendChild(price);

        // Кнопка
        const btn = document.createElement('button');
        btn.className = 'btn-course-details';
        btn.textContent = 'Подробнее';
        card.appendChild(btn);

        container.appendChild(card);
    });
}


function updateSuggestions(courses) {
    suggestions.innerHTML = '';
    const titles = [...new Set(courses.map(c => c.title))];
    titles.forEach(title => {
        suggestions.innerHTML += `<option value="${title}">`;
    });
}

// debounce
function delayedFetch() {
    clearTimeout(timeout);
    timeout = setTimeout(fetchCourses, 300);
}

const clearSearchBtn = document.getElementById('clear-search');

clearSearchBtn.addEventListener('click', () => {
    searchInput.value = '';
    fetchCourses(); // обновляем список курсов после очистки
});


// listeners
searchInput.addEventListener('input', delayedFetch);
levelSelect.addEventListener('change', fetchCourses);
priceSelect.addEventListener('change', fetchCourses);
durationSelect.addEventListener('change', fetchCourses);
