document.addEventListener('DOMContentLoaded', () => {
    // Вкладки
    const tabs = document.querySelectorAll('.tab-btn');
    const contents = document.querySelectorAll('#tab-content > div');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Снимаем активный класс со всех вкладок
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            // Показываем соответствующий контент
            const target = tab.dataset.tab;
            contents.forEach(c => {
                c.style.display = (c.classList.contains(target)) ? 'block' : 'none';
            });
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const avatarInput = document.getElementById('avatarInput');
    const avatarPreview = document.getElementById('avatarPreview');
    const changeAvatarBtn = document.getElementById('changeAvatarBtn');
    const cancelBtn = document.getElementById('cancelProfileChanges');
    const saveBtn = document.getElementById('saveProfileChanges');

    let selectedAvatarFile = null;

    // открыть выбор файла
    changeAvatarBtn.addEventListener('click', () => {
        avatarInput.click();
    });

    // превью аватара
    avatarInput.addEventListener('change', () => {
        const file = avatarInput.files[0];
        if (!file) return;

        if (!['image/jpeg', 'image/png'].includes(file.type)) {
            alert('Допустимы только JPG и PNG');
            avatarInput.value = '';
            return;
        }

        if (file.size > 2 * 1024 * 1024) {
            alert('Максимальный размер файла — 2MB');
            avatarInput.value = '';
            return;
        }

        selectedAvatarFile = file;

        const reader = new FileReader();
        reader.onload = e => {
            avatarPreview.src = e.target.result;
        };
        reader.readAsDataURL(file);
    });

    // отмена — вернуть старые данные
    cancelBtn.addEventListener('click', () => {
        avatarPreview.src = avatarPreview.dataset.original;
        avatarInput.value = '';
        selectedAvatarFile = null;

        document.getElementById('profileForm').reset();
    });

    // сохранить изменения
    saveBtn.addEventListener('click', async () => {
        const formData = new FormData(document.getElementById('profileForm'));

        if (selectedAvatarFile) {
            formData.append('avatar', selectedAvatarFile);
        }

        const response = await fetch('/profile/update', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            location.reload();
        } else {
            alert('Ошибка сохранения профиля');
        }
    });
});

const inputAvatar = document.getElementById('inputAvatar');
const btnChangePhoto = document.getElementById('btnChangePhoto');
const avatarModal = document.getElementById('avatarModal');
const cropImage = document.getElementById('cropImage');
const saveCrop = document.getElementById('saveCrop');
const cancelCrop = document.getElementById('cancelCrop');
const avatarPreview = document.getElementById('avatarPreview');
const canvas = document.getElementById('avatarCanvas');
const ctx = canvas.getContext('2d');
const wrapper = document.querySelector('.avatar-crop-wrapper');

let scale = 1;
let minScale = 1;
let posX = 0;
let posY = 0;
let dragging = false;
let startX, startY;

btnChangePhoto.onclick = () => inputAvatar.click();

inputAvatar.onchange = e => {
    const file = e.target.files[0];
    if (!file) return;

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

    update();
}

function update() {
    cropImage.style.transform =
        `translate(-50%, -50%) translate(${posX}px, ${posY}px) scale(${scale})`;
}

/* drag */
wrapper.onmousedown = e => {
    dragging = true;
    startX = e.clientX - posX;
    startY = e.clientY - posY;
};

document.onmousemove = e => {
    if (!dragging) return;
    posX = e.clientX - startX;
    posY = e.clientY - startY;
    update();
};

document.onmouseup = () => dragging = false;

/* zoom колесиком */
wrapper.onwheel = e => {
    e.preventDefault();
    const delta = e.deltaY > 0 ? -0.05 : 0.05;
    scale = Math.max(minScale, scale + delta);
    update();
};

/* сохранение */
saveCrop.onclick = () => {
    canvas.width = 300;
    canvas.height = 300;

    ctx.clearRect(0,0,300,300);
    ctx.save();
    ctx.beginPath();
    ctx.arc(150,150,150,0,Math.PI*2);
    ctx.clip();

    const imgW = cropImage.naturalWidth * scale;
    const imgH = cropImage.naturalHeight * scale;

    const dx = 150 - imgW / 2 + posX;
    const dy = 150 - imgH / 2 + posY;

    ctx.drawImage(
        cropImage,
        dx,
        dy,
        imgW,
        imgH
    );

    ctx.restore();

    avatarPreview.src = canvas.toDataURL('image/png');
    avatarModal.style.display = 'none';
};

cancelCrop.onclick = () => {
    avatarModal.style.display = 'none';
};

