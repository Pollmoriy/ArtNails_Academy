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

        reviews.forEach(r => {
            const card = document.createElement('div');
            card.className = 'review-card';

            card.innerHTML = `
                <img class="review-avatar"
                     src="${r.avatar ? `/static/${r.avatar}` : '/static/img/default_avatar.png'}">

                <div class="review-header">
                    <div class="review-name">${r.user_name}</div>
                    <div class="review-course">${r.course_title}</div>
                </div>

                <div class="review-stars">
                    ${[1,2,3,4,5].map(i =>
                        `<img class="star"
                         src="/static/icons/${i <= r.rating ? 'star-filled' : 'star-empty'}.svg">`
                    ).join('')}
                </div>

                <div class="review-date">${r.created_at}</div>
                <p class="review-text">${r.comment}</p>
            `;

            reviewsContainer.appendChild(card);
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
            for (let i = 0; i < selectedRating; i++) {
                stars[i].classList.add('selected');
            }
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
            body: JSON.stringify({
                course_id: courseId,
                rating: selectedRating,
                comment: comment
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                modal.style.display = 'none';
                document.getElementById('review-comment').value = '';
                stars.forEach(s => s.classList.remove('selected'));
                selectedRating = 0;
                fetchReviews();
            } else {
                alert('Ошибка при добавлении отзыва');
            }
        });
    });

});
