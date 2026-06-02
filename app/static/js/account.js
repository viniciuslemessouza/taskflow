const input = document.getElementById('profile_picture');
const preview = document.getElementById('profile-preview');

input.addEventListener('change', function () {
    const file = this.files[0];

    if (!file) return;

    preview.src = URL.createObjectURL(file);
});