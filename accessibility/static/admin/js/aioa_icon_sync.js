
document.addEventListener('DOMContentLoaded', function () {

    // ============================
    // HANDLE ICON TYPE SELECTION
    // ============================
    const iconTypeRadios = document.querySelectorAll('input[name="aioa_icon_type"]');

    iconTypeRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            // Remove 'selected' class from all icon-type options
            document.querySelectorAll('.icon-select-wrapper .icon-option')
                .forEach(el => el.classList.remove('selected'));

            // Add 'selected' class to the clicked one
            if (radio.checked) {
                radio.closest('.icon-option').classList.add('selected');
            }

            // Get selected icon image URL
            const selectedIconUrl = radio.nextElementSibling.getAttribute('src');

            // Update all icon-size previews to match selected icon
            const iconSizeImages = document.querySelectorAll('.aioa-icon-img-size');
            iconSizeImages.forEach(img => {
                const size = img.parentElement.getAttribute('data-size');
                img.setAttribute('src', selectedIconUrl);
                img.setAttribute('style', `width:${size}px;height:${size}px;`);
            });
        });
    });

    // Highlight selected icon-type on initial load
    document.querySelectorAll('input[name="aioa_icon_type"]:checked')
        .forEach(radio => radio.closest('.icon-option').classList.add('selected'));


    // ============================
    // HANDLE ICON SIZE SELECTION
    // ============================
    const iconSizeRadios = document.querySelectorAll('input[name="aioa_icon_size"]');

    iconSizeRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            // Remove 'selected' class from all icon-size options
            document.querySelectorAll('.icon-size-select-wrapper .icon-option')
                .forEach(el => el.classList.remove('selected'));

            // Add 'selected' class to the clicked one
            if (radio.checked) {
                radio.closest('.icon-option').classList.add('selected');
            }
        });
    });

    // Highlight selected icon-size on initial load
    document.querySelectorAll('input[name="aioa_icon_size"]:checked')
        .forEach(radio => radio.closest('.icon-option').classList.add('selected'));
});


