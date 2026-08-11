// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function () {
    // Insert the upgrade/notice banner at the top of the settings form
    const insertNoticeBanner = () => {
        if (document.querySelector('.aioa-card')) {
            return; // already inserted
        }

        const fieldset = document.querySelector('#content-main form fieldset')
            || document.querySelector('.module.aligned')
            || document.querySelector('#content-main form');

        if (!fieldset) {
            return;
        }

        const noticeHTML = `
<p class="aioa-card" style="margin: 0 0 6px 0; color: inherit; font-size: 0.9rem; line-height: 1.55;">
  <strong>NOTE:</strong>
  Currently, All in One Accessibility is dedicated to enhancing accessibility specifically for
  websites and online stores. Please upgrade to the full version of
  <a href="https://ada.skynettechnologies.us/trial-subscription" target="_blank"
     style="color: #9b6dff; font-weight: 600; text-decoration: underline;">
    All in One Accessibility Pro with 10 days free trial
  </a>.
</p>
<p class="aioa-card" style="margin: 0 0 16px 0; color: inherit; font-size: 0.9rem; line-height: 1.55; opacity: 0.85;">
  It may take a few seconds for changes to appear on your website. If you don't see the
  changes, try clearing your browser cache or checking in a private browsing window.
</p>`;

        fieldset.insertAdjacentHTML('beforebegin', noticeHTML);
    };

    try {
        insertNoticeBanner();
    } catch (error) {
        console.error('AIOA: Error inserting notice banner:', error);
    }

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