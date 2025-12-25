document.addEventListener('DOMContentLoaded', () => {

    const courseSelect = document.getElementById('review-course-filter');
    const sortSelect = document.getElementById('review-sort-filter');
    const reviewsContainer = document.getElementById('reviews-container');

    const addReviewBtn = document.querySelector('.btn-add-review');
    const modal = document.getElementById('add-review-modal');
    const closeModalBtn = document.getElementById('close-review-modal');
    const submitReviewBtn = document.getElementById('submit-review');

    const stars = document.querySelectorAll('#review-rating .star');
    let selectedRating = 0;

    // ===== ФИЛЬТРЫ =====
    function fetchReviews() {
        const params = new URLSearchParams({
            course: courseSelect.value,
            sort: sortSelect.value
        });

        fetch(`/reviews?${params.toString()}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(res => res.json())
        .then(renderReviews)
        .catch(err => console.error(err));
    }

    function renderReviews(reviews) {
        reviewsContainer.innerHTML = '';

        if (!reviews.length) {
            reviewsContainer.innerHTML = '<p>Отзывы не найдены</p>';
            return;
        }

        reviews.forEach((r, i) => {
            const card = document.createElement('div');
            card.className = 'review-card';
            card.dataset.reviewId = r.id;

            // Сразу ставим начальные стили для анимации
            card.style.opacity = 0;
            card.style.transform = 'translateY(20px)';

            card.innerHTML = `
                <img class="review-avatar" src="${r.avatar ? `/static/${r.avatar}` : '/static/img/default_avatar.png'}">
                <div class="review-header">
                    <div class="review-name">${r.user_name}</div>
                    <div class="review-course">${r.course_title}</div>
                </div>
                <div class="review-stars">
                    ${[1,2,3,4,5].map(i =>
                        `<img class="star" src="/static/icons/${i <= r.rating ? 'star-filled' : 'star-empty'}.svg">`
                    ).join('')}
                </div>
                <div class="review-date">${r.created_at}</div>
                <p class="review-text">${r.comment}</p>
            `;

            // Кнопка удаления
            if (r.is_owner) {
                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'btn-delete-review';
                deleteBtn.textContent = 'Удалить';
                deleteBtn.style.opacity = 0;
                deleteBtn.style.transform = 'translateY(20px)';
                card.appendChild(deleteBtn);
            }

            reviewsContainer.appendChild(card);

            // Анимация с задержкой для плавного появления
            setTimeout(() => {
                card.style.transition = 'all 0.6s ease';
                card.style.opacity = 1;
                card.style.transform = 'translateY(0)';

                const avatar = card.querySelector('.review-avatar');
                const header = card.querySelector('.review-header');
                const starsElem = card.querySelector('.review-stars');
                const date = card.querySelector('.review-date');
                const text = card.querySelector('.review-text');
                const deleteBtn = card.querySelector('.btn-delete-review');

                if (avatar) setTimeout(() => { avatar.style.opacity = 1; avatar.style.transform = 'translateY(0)'; }, 100);
                if (header) setTimeout(() => { header.style.opacity = 1; header.style.transform = 'translateY(0)'; }, 200);
                if (starsElem) setTimeout(() => { starsElem.style.opacity = 1; starsElem.style.transform = 'translateY(0)'; }, 300);
                if (date) setTimeout(() => { date.style.opacity = 1; date.style.transform = 'translateY(0)'; }, 400);
                if (text) setTimeout(() => { text.style.opacity = 1; text.style.transform = 'translateY(0)'; }, 500);
                if (deleteBtn) setTimeout(() => { deleteBtn.style.opacity = 1; deleteBtn.style.transform = 'translateY(0)'; }, 600);

            }, i * 150);
        });
    }

    courseSelect.addEventListener('change', fetchReviews);
    sortSelect.addEventListener('change', fetchReviews);

    fetchReviews();

    // ===== МОДАЛКА =====
    addReviewBtn.addEventListener('click', () => {
        modal.style.display = 'flex';
    });
    closeModalBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    stars.forEach(star => {
        star.addEventListener('click', () => {
            selectedRating = +star.dataset.value;
            stars.forEach(s => s.classList.remove('selected'));
            for (let i = 0; i < selectedRating; i++) stars[i].classList.add('selected');
        });
    });

    submitReviewBtn.addEventListener('click', () => {
        const courseId = document.getElementById('review-course').value;
        const comment = document.getElementById('review-comment').value.trim();

        if (!courseId || !selectedRating || !comment) {
            alert('Заполните все поля');
            return;
        }

        fetch('/reviews/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ course_id: courseId, rating: selectedRating, comment })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                modal.style.display = 'none';
                document.getElementById('review-comment').value = '';
                stars.forEach(s => s.classList.remove('selected'));
                selectedRating = 0;
                fetchReviews();
            } else alert('Ошибка при добавлении отзыва');
        });
    });

});

// ===== УДАЛЕНИЕ ОТЗЫВА =====
document.addEventListener('click', function (e) {
    if (!e.target.classList.contains('btn-delete-review')) return;

    const card = e.target.closest('.review-card');
    const reviewId = card.dataset.reviewId;

    if (!reviewId) return;

    const confirmDelete = confirm('Удалить этот отзыв?');
    if (!confirmDelete) return;

    fetch('/reviews/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ review_id: reviewId })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) card.remove();
        else alert(data.error || 'Ошибка при удалении');
    })
    .catch(err => {
        console.error(err);
        alert('Ошибка сети');
    });
});
