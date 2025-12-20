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
        container.innerHTML += `
            <div class="course-card">
                <img src="/static/${course.image}">
                <div class="course-top-info">
                    <span>${course.difficulty}</span>
                    <span>${course.duration_weeks} нед.</span>
                </div>
                <h3>${course.title}</h3>
                <p>${course.short_description}</p>
                <span>${course.price} BYN</span>
                <button class="btn-course-details">Подробнее</button>
            </div>
        `;
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

// listeners
searchInput.addEventListener('input', delayedFetch);
levelSelect.addEventListener('change', fetchCourses);
priceSelect.addEventListener('change', fetchCourses);
durationSelect.addEventListener('change', fetchCourses);
