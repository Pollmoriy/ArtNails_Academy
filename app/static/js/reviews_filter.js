const courseSelect = document.getElementById('review-course-filter');
const sortSelect = document.getElementById('review-sort-filter');
const reviewsContainer = document.getElementById('reviews-container');

function fetchReviews() {
    const courseId = courseSelect.value;
    const sort = sortSelect.value;

    // Параметры для запроса
    const params = new URLSearchParams({
        course: courseId,
        sort: sort
    });

    fetch(`/reviews?${params.toString()}`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(res => res.json())
    .then(data => renderReviews(data))
    .catch(err => console.error(err));
}

function renderReviews(reviews) {
    reviewsContainer.innerHTML = '';

    if (reviews.length === 0) {
        reviewsContainer.innerHTML = '<p>Отзывы не найдены</p>';
        return;
    }

    reviews.forEach(r => {
        const card = document.createElement('div');
        card.className = 'review-card';

        // Аватар
        const avatar = document.createElement('img');
        avatar.className = 'review-avatar';
        avatar.src = r.avatar ? `/static/${r.avatar}` : '/static/img/default_avatar.png';
        avatar.alt = 'avatar';
        card.appendChild(avatar);

        // Хедер
        const header = document.createElement('div');
        header.className = 'review-header';

        const name = document.createElement('div');
        name.className = 'review-name';
        name.textContent = r.user_name;

        const courseTitle = document.createElement('div');
        courseTitle.className = 'review-course';
        courseTitle.textContent = r.course_title;

        header.appendChild(name);
        header.appendChild(courseTitle);
        card.appendChild(header);

        // Звезды
        const stars = document.createElement('div');
        stars.className = 'review-stars';
        for (let i = 1; i <= 5; i++) {
            const star = document.createElement('img');
            star.className = 'star';
            star.src = i <= r.rating ? '/static/icons/star-filled.svg' : '/static/icons/star-empty.svg';
            star.alt = 'star';
            stars.appendChild(star);
        }
        card.appendChild(stars);

        // Дата
        const date = document.createElement('div');
        date.className = 'review-date';
        date.textContent = r.created_at;
        card.appendChild(date);

        // Комментарий
        const comment = document.createElement('p');
        comment.className = 'review-text';
        comment.textContent = r.comment;
        card.appendChild(comment);

        reviewsContainer.appendChild(card);
    });
}

// События для фильтров
courseSelect.addEventListener('change', fetchReviews);
sortSelect.addEventListener('change', fetchReviews);

// Первичная загрузка
fetchReviews();
