// ==========================
// Вкладки курса и анимации
// ==========================
document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.tab-content');
    const activeLine = document.querySelector('.active-line');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Снимаем active со всех вкладок и контента
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));

            // Активируем текущую вкладку и контент
            tab.classList.add('active');
            const tabName = tab.dataset.tab;
            const content = document.getElementById(tabName + '-content');
            content.classList.add('active');

            // Анимация элементов вкладки
            if (tabName === 'overview') animateOverview(content);
            if (tabName === 'program') animateModules(content);
            if (tabName === 'teacher') animateTeacher(content);
            if (tabName === 'reviews') animateReviews(content);

            // Линия под активной вкладкой
            activeLine.style.width = tab.offsetWidth + 'px';
            activeLine.style.left = tab.offsetLeft + 'px';
        });
    });

    // Линия под первой вкладкой при загрузке
    const initialTab = document.querySelector('.tab.active');
    activeLine.style.width = initialTab.offsetWidth + 'px';
    activeLine.style.left = initialTab.offsetLeft + 'px';

    // Анимация активной вкладки при загрузке
    const activeContent = document.querySelector('.tab-content.active');
    if (activeContent) {
        if (activeContent.id === 'overview-content') animateOverview(activeContent);
        if (activeContent.id === 'program-content') animateModules(activeContent);
        if (activeContent.id === 'teacher-content') animateTeacher(activeContent);
        if (activeContent.id === 'reviews-content') animateReviews(activeContent);
    }
});

// ==========================
// Анимации
// ==========================
function animateOverview(content) {
    const learningItems = content.querySelectorAll(".learning-outcomes .column p");
    const requirements = content.querySelectorAll(".requirements p");
    const statsRows = content.querySelectorAll(".course-stats-row");

    let delay = 0;
    [...learningItems, ...requirements, ...statsRows].forEach(el => {
        el.style.opacity = 0;
        el.style.transform = "translateY(20px)";
        setTimeout(() => {
            el.style.transition = "all 0.6s ease";
            el.style.opacity = 1;
            el.style.transform = "translateY(0)";
        }, delay += 150);
    });
}

function animateModules(content) {
    const modules = content.querySelectorAll(".modules-wrapper .module-card");
    let delay = 0;
    modules.forEach(el => {
        el.style.opacity = 0;
        el.style.transform = "translateY(20px)";
        setTimeout(() => {
            el.style.transition = "all 0.6s ease";
            el.style.opacity = 1;
            el.style.transform = "translateY(0)";
        }, delay += 150);
    });
}

function animateTeacher(content) {
    const photo = content.querySelector(".teacher-photo");
    const info = content.querySelector(".teacher-info");
    const bio = content.querySelector(".teacher-bio");

    [photo, info, bio].forEach(el => {
        el.style.opacity = 0;
        el.style.transform = "translateY(20px)";
    });

    setTimeout(() => {
        photo.style.transition = info.style.transition = bio.style.transition = "all 0.6s ease";
        photo.style.opacity = 1; photo.style.transform = "translateY(0)";
        info.style.opacity = 1; info.style.transform = "translateY(0)";
        bio.style.opacity = 1; bio.style.transform = "translateY(0)";
    }, 100);
}
function animateReviews(content) {
    const reviewCards = content.querySelectorAll(".review-card");

    let globalDelay = 0;

    reviewCards.forEach(card => {
        // элементы внутри карточки
        const avatar = card.querySelector(".review-avatar");
        const header = card.querySelector(".review-header");
        const stars = card.querySelector(".review-stars");
        const date = card.querySelector(".review-date");
        const text = card.querySelector(".review-text");
        const deleteBtn = card.querySelector(".btn-delete-review");

        const elements = [avatar, header, stars, date, text, deleteBtn].filter(Boolean);

        // начальное состояние
        card.style.opacity = 1;
        elements.forEach(el => {
            el.style.opacity = 0;
            el.style.transform = "translateY(16px)";
        });

        // небольшая задержка между карточками
        setTimeout(() => {
            let innerDelay = 0;

            elements.forEach(el => {
                setTimeout(() => {
                    el.style.transition = "opacity 0.5s ease, transform 0.5s ease";
                    el.style.opacity = 1;
                    el.style.transform = "translateY(0)";
                }, innerDelay);

                innerDelay += 100;
            });

        }, globalDelay);

        globalDelay += 180;
    });
}
