document.addEventListener('DOMContentLoaded', () => {

    /* =======================
       ВКЛАДКИ
    ======================= */
    const tabs = document.querySelectorAll('.tab-btn');
    const contents = document.querySelectorAll('#tab-content > div');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            const target = tab.dataset.tab;
            contents.forEach(c => {
                c.style.display = c.classList.contains(target) ? 'block' : 'none';
            });
        });
    });

    // Показываем первую вкладку по умолчанию
    tabs[0].click();


    /* =======================
       АВАТАР: ВЫБОР И ОБРЕЗКА
    ======================= */
    const inputAvatar = document.getElementById('inputAvatar');
    const btnChangePhoto = document.getElementById('btnChangePhoto');
    const avatarModal = document.getElementById('avatarModal');
    const cropImage = document.getElementById('cropImage');
    const saveCrop = document.getElementById('saveCrop');
    const cancelCrop = document.getElementById('cancelCrop');
    const avatarPreview = document.getElementById('profileAvatar');
    const zoomRange = document.getElementById('zoomRange');
    const canvas = document.getElementById('avatarCanvas');
    const wrapper = document.querySelector('.avatar-crop-wrapper');
    const ctx = canvas.getContext('2d');

    let scale = 1;
    let minScale = 1;
    let posX = 0;
    let posY = 0;
    let dragging = false;
    let startX = 0;
    let startY = 0;
    let originalAvatarSrc = avatarPreview.src;

    // Глобально для отправки на сервер
    window.croppedAvatarBlob = null;

    // открыть выбор файла
    btnChangePhoto.onclick = () => inputAvatar.click();

    inputAvatar.onchange = e => {
        const file = e.target.files[0];
        if (!file) return;

        originalAvatarSrc = avatarPreview.src; // сохраняем текущий аватар

        const reader = new FileReader();
        reader.onload = () => {
            cropImage.onload = initImage;
            cropImage.src = reader.result;
            avatarModal.style.display = 'flex';
        };
        reader.readAsDataURL(file);
    };

    function initImage() {
        const w = cropImage.naturalWidth;
        const h = cropImage.naturalHeight;
        const size = wrapper.offsetWidth;

        minScale = Math.max(size / w, size / h);
        scale = minScale;

        posX = 0;
        posY = 0;

        updateTransform();
        zoomRange.value = 1;
    }

    function updateTransform() {
        cropImage.style.transform =
            `translate(-50%, -50%) translate(${posX}px, ${posY}px) scale(${scale})`;
    }

    // Перетаскивание
    wrapper.onmousedown = e => {
        dragging = true;
        startX = e.clientX - posX;
        startY = e.clientY - posY;
        wrapper.style.cursor = 'grabbing';
    };
    document.onmousemove = e => {
        if (!dragging) return;
        posX = e.clientX - startX;
        posY = e.clientY - startY;
        updateTransform();
    };
    document.onmouseup = () => {
        dragging = false;
        wrapper.style.cursor = 'grab';
    };

    // Зум колесиком
    wrapper.onwheel = e => {
        e.preventDefault();
        const delta = e.deltaY > 0 ? -0.05 : 0.05;
        scale = Math.max(minScale, scale + delta);
        updateTransform();
    };

    // Зум через слайдер
    zoomRange.oninput = e => {
        const value = parseFloat(e.target.value);
        scale = minScale * value;
        updateTransform();
    };

    // Отмена обрезки
    cancelCrop.onclick = () => {
        avatarModal.style.display = 'none';
        cropImage.src = '';
        avatarPreview.src = originalAvatarSrc;
        window.croppedAvatarBlob = null;
    };

    // Сохранение обрезки
    saveCrop.onclick = () => {
        const size = 300;
        canvas.width = size;
        canvas.height = size;

        ctx.clearRect(0, 0, size, size);
        ctx.save();
        ctx.beginPath();
        ctx.arc(size / 2, size / 2, size / 2, 0, Math.PI * 2);
        ctx.clip();

        const imgW = cropImage.naturalWidth * scale;
        const imgH = cropImage.naturalHeight * scale;
        const dx = size / 2 - imgW / 2 + posX;
        const dy = size / 2 - imgH / 2 + posY;

        ctx.drawImage(cropImage, dx, dy, imgW, imgH);
        ctx.restore();

        avatarPreview.src = canvas.toDataURL('image/png');

        canvas.toBlob(blob => {
            window.croppedAvatarBlob = blob;
        }, 'image/png');

        avatarModal.style.display = 'none';
    };


    /* =======================
       ПРОФИЛЬ: ОТМЕНА / СОХРАНЕНИЕ
    ======================= */
    const nameInput = document.getElementById('profileName');
    const lastNameInput = document.getElementById('profileLastName');
    const emailInput = document.getElementById('profileEmail');
    const btnCancel = document.getElementById('btnCancel');
    const btnSave = document.getElementById('btnSave');

    // Сохраняем исходные данные
    const initialState = {
    name: nameInput.value,
    lastName: lastNameInput.value,
    email: emailInput.value,
    avatar: avatarPreview.src
};


    // Отмена изменений
    btnCancel.addEventListener('click', () => {
    nameInput.value = initialState.name;
    lastNameInput.value = initialState.lastName;
    emailInput.value = initialState.email;
    avatarPreview.src = initialState.avatar;
    window.croppedAvatarBlob = null;
});


    // Сохранение изменений
   btnSave.addEventListener('click', async () => {
    const formData = new FormData();
    formData.append('first_name', nameInput.value);
    formData.append('last_name', lastNameInput.value);
    formData.append('email', emailInput.value);

    if (window.croppedAvatarBlob) {
        formData.append('avatar', window.croppedAvatarBlob, 'avatar.png');
    }

    try {
        const response = await fetch('/profile/update', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            // 🔹 обновляем состояние БЕЗ перезагрузки
            initialState.name = nameInput.value;
            initialState.lastName = lastNameInput.value;
            initialState.email = emailInput.value;

            if (result.avatar_url) {
                avatarPreview.src = result.avatar_url;
                initialState.avatar = result.avatar_url;
            }

            alert('Изменения сохранены');
        } else {
            alert(result.message || 'Ошибка сохранения');
        }
    } catch {
        alert('Ошибка соединения с сервером');
    }
});


});
