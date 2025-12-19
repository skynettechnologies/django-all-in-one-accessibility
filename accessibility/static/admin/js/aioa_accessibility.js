// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function () {
    const toggleFields = () => {
        // Get toggle field elements
        const enablePosition = document.querySelector('#id_enable_widget_icon_position');
        const enableCustomSize = document.querySelector('#id_enable_icon_custom_size');

        // Position-related fields
        const rightPx = document.querySelector('.form-row.field-to_the_right_px');
        const rightDir = document.querySelector('.form-row.field-to_the_right');
        const bottomPx = document.querySelector('.form-row.field-to_the_bottom_px');
        const bottomDir = document.querySelector('.form-row.field-to_the_bottom');
        const positionField = document.querySelector('.form-row.field-aioa_place');

        // Icon-size related fields
        const iconSizeVal = document.querySelector('.form-row.field-aioa_size_value');
        const iconSizeSel = document.querySelector('.form-row.field-aioa_icon_size');

        // Toggle position fields
        if (enablePosition.checked) {
            rightPx.style.display = '';
            rightDir.style.display = '';
            bottomPx.style.display = '';
            bottomDir.style.display = '';
            positionField.style.display = 'none';
        } else {
            rightPx.style.display = 'none';
            rightDir.style.display = 'none';
            bottomPx.style.display = 'none';
            bottomDir.style.display = 'none';
            positionField.style.display = '';
        }

        // Toggle icon size fields
        if (enableCustomSize.checked) {
            iconSizeVal.style.display = '';
            iconSizeSel.style.display = 'none';
        } else {
            iconSizeVal.style.display = 'none';
            iconSizeSel.style.display = '';
        }
    };

    // Initial toggle
    toggleFields();

    // Add event listeners
    document.querySelector('#id_enable_widget_icon_position').addEventListener('change', toggleFields);
    document.querySelector('#id_enable_icon_custom_size').addEventListener('change', toggleFields);
});
