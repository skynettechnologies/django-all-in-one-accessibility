// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function () {
    const toggleFields = () => {
        // Get toggle field elements
        const enablePosition = document.querySelector('#id_enable_widget_icon_position');
        const enableCustomSize = document.querySelector('#id_enable_icon_custom_size');

        // Exit early if toggles don't exist
        if (!enablePosition || !enableCustomSize) {
            console.warn('AIOA: Toggle checkboxes not found');
            return;
        }

        // Position-related fields
        const rightPx = document.querySelector('.form-row.field-to_the_right_px');
        const rightDir = document.querySelector('.form-row.field-to_the_right');
        const bottomPx = document.querySelector('.form-row.field-to_the_bottom_px');
        const bottomDir = document.querySelector('.form-row.field-to_the_bottom');
        const positionField = document.querySelector('.form-row.field-aioa_place');

        // Icon-size related fields
        const iconSizeVal = document.querySelector('.form-row.field-aioa_size_value');
        const iconSizeSel = document.querySelector('.form-row.field-aioa_icon_size');

        // Toggle position fields with null checks
        if (enablePosition.checked) {
            if (rightPx) rightPx.style.display = '';
            if (rightDir) rightDir.style.display = '';
            if (bottomPx) bottomPx.style.display = '';
            if (bottomDir) bottomDir.style.display = '';
            if (positionField) positionField.style.display = 'none';
        } else {
            if (rightPx) rightPx.style.display = 'none';
            if (rightDir) rightDir.style.display = 'none';
            if (bottomPx) bottomPx.style.display = 'none';
            if (bottomDir) bottomDir.style.display = 'none';
            if (positionField) positionField.style.display = '';
        }

        // Toggle icon size fields with null checks
        if (enableCustomSize.checked) {
            if (iconSizeVal) iconSizeVal.style.display = '';
            if (iconSizeSel) iconSizeSel.style.display = 'none';
        } else {
            if (iconSizeVal) iconSizeVal.style.display = 'none';
            if (iconSizeSel) iconSizeSel.style.display = '';
        }
    };

    // Initial toggle
    try {
        toggleFields();
    } catch (error) {
        console.error('AIOA: Error during initial field toggle:', error);
    }

    // Add event listeners with error handling
    const enablePositionCheckbox = document.querySelector('#id_enable_widget_icon_position');
    const enableCustomSizeCheckbox = document.querySelector('#id_enable_icon_custom_size');
    
    if (enablePositionCheckbox) {
        enablePositionCheckbox.addEventListener('change', function() {
            try {
                toggleFields();
            } catch (error) {
                console.error('AIOA: Error toggling position fields:', error);
            }
        });
    }
    
    if (enableCustomSizeCheckbox) {
        enableCustomSizeCheckbox.addEventListener('change', function() {
            try {
                toggleFields();
            } catch (error) {
                console.error('AIOA: Error toggling icon size fields:', error);
            }
        });
    }
});
