// ==========================
// Переменные
// ==========================
const searchInput = document.getElementById('search');
const levelSelect = document.getElementById('level');
const priceSelect = document.getElementById('price');
const durationSelect = document.getElementById('duration');
const container = document.getElementById('courses-container');
const suggestions = document.getElementById('search-suggestions');
const clearSearchBtn = document.getElementById('clear-search');

let timeout = null;

// ==========================
// Настройка контейнера
// ==========================
container.style.display = 'grid';
container.style.gridTemplateColumns = 'repeat(3, 1fr)';
container.style.gap = '32px';
container.style.justifyContent = 'center'; // центрирование при <3 карточках

// ==========================
// Fetch
// ==========================
function fetchCourses() {
    const params = new URLSearchParams({
        search: searchInput.value,
        level: levelSelect.value,
        price: priceSelect.value,
        duration: durationSelect.value
    });

    container.classList.add('loading');

    fetch(`/catalog?${params.toString()}`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
        .then(res => res.json())
        .then(data => {
            renderCourses(data);
            updateSuggestions(data);
            requestAnimationFrame(() => {
                animateCards();
            });
            container.classList.remove('loading');
        });
}

// ==========================
// Render
// ==========================
function renderCourses(courses) {
    container.innerHTML = '';

    if (!courses.length) {
        container.innerHTML = '<p class="no-results">Курсы не найдены</p>';
        return;
    }

    courses.forEach(course => {
        const card = document.createElement('div');
        card.className = 'course-card public-course-card';
        card.style.width = '100%'; // чтобы занимала одну колонку грид

        card.innerHTML = `
            <img class="course-img" src="/static/${course.image}" alt="${course.title}">

            <div class="course-top-info">
                <span class="course-level">${course.difficulty}</span>
                <span class="course-duration">${course.duration_weeks} недели</span>
            </div>

            <h3 class="course-name">${course.title}</h3>
            <p class="course-desc">${course.short_description}</p>
            <span class="course-price">${course.price} BYN</span>

            <a href="/course/${course.id_course}" class="btn-course-details">
                Подробнее
            </a>
        `;

        // начальное состояние ВСЕХ элементов
        card.style.opacity = 0;
        card.style.transform = 'translateY(20px)';

        card.querySelectorAll(
            '.course-name, .course-desc, .course-price, .btn-course-details'
        ).forEach(el => {
            el.style.opacity = 0;
            el.style.transform = 'translateY(10px)';
        });

        container.appendChild(card);
    });
}

// ==========================
// Анимация карточек
// ==========================
function animateCards() {
    const cards = container.querySelectorAll('.course-card');

    cards.forEach((card, i) => {
        setTimeout(() => {
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            card.style.opacity = 1;
            card.style.transform = 'translateY(0)';

            const inner = card.querySelectorAll(
                '.course-name, .course-desc, .course-price, .btn-course-details'
            );

            inner.forEach((el, j) => {
                setTimeout(() => {
                    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                    el.style.opacity = 1;
                    el.style.transform = 'translateY(0)';
                }, j * 80);
            });
        }, i * 150); // задержка между карточками
    });
}

// ==========================
// Suggestions
// ==========================
function updateSuggestions(courses) {
    suggestions.innerHTML = '';
    [...new Set(courses.map(c => c.title))].forEach(title => {
        const option = document.createElement('option');
        option.value = title;
        suggestions.appendChild(option);
    });
}

// ==========================
// Debounce
// ==========================
function delayedFetch() {
    clearTimeout(timeout);
    timeout = setTimeout(fetchCourses, 300);
}

// ==========================
// Listeners
// ==========================
searchInput.addEventListener('input', delayedFetch);
levelSelect.addEventListener('change', fetchCourses);
priceSelect.addEventListener('change', fetchCourses);
durationSelect.addEventListener('change', fetchCourses);

clearSearchBtn.addEventListener('click', () => {
    searchInput.value = '';
    fetchCourses();
});

// ==========================
// Initial animation
// ==========================
document.addEventListener("DOMContentLoaded", () => {
    animateCards();
});
