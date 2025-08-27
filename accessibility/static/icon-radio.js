document.addEventListener('DOMContentLoaded', function() {
    const radios = document.querySelectorAll('.icon-checkmark').length > 0;
    document.querySelectorAll('input[type=radio]').forEach(radio => {
        radio.addEventListener('change', function() {
            // Hide all checkmarks
            document.querySelectorAll('.icon-checkmark').forEach(c => c.style.display = 'none');
            // Show checkmark only for selected radio
            const selectedIcon = this.closest('label').querySelector('.icon-checkmark');
            if (selectedIcon) selectedIcon.style.display = 'flex';
        });
    });
});



document.addEventListener('DOMContentLoaded', function () {
  const radios = document.querySelectorAll('input[type="radio"]');

  radios.forEach(radio => {
    radio.addEventListener('change', function () {
      document.querySelectorAll('.icon-radio').forEach(label => {
        label.style.border = '4px solid transparent'; // Reset border
        const checkmark = label.querySelector('.icon-checkmark');
        if (checkmark) checkmark.style.display = 'none'; // Hide checkmark
      });

      const selectedLabel = this.closest('.icon-radio');
      if (selectedLabel) {
        selectedLabel.style.border = '4px solid #137333'; // ✅ Green border for selected
        const checkmark = selectedLabel.querySelector('.icon-checkmark');
        if (checkmark) checkmark.style.display = 'flex'; // ✅ Show checkmark
      }
    });
  });

  // Ensure correct border/checkmark on page load if any pre-selected
  const checked = document.querySelector('input[type="radio"]:checked');
  if (checked) {
    checked.dispatchEvent(new Event('change'));
  }
});


document.addEventListener("DOMContentLoaded", function () {
  function updateAllRadioGroups() {
    const allRadios = document.querySelectorAll('.icon-radio input[type="radio"]');

    allRadios.forEach(radio => {
      const label = radio.closest('.icon-radio');
      const checkmark = label.querySelector('.icon-checkmark');

      if (radio.checked) {
        label.style.borderColor = '#137333';
        label.style.borderWidth = '4px';
        if (checkmark) checkmark.style.display = 'flex';
      } else {
        label.style.borderColor = 'transparent';
        if (checkmark) checkmark.style.display = 'none';
      }
    });
  }

  const allRadios = document.querySelectorAll('.icon-radio input[type="radio"]');
  allRadios.forEach(radio => {
    radio.addEventListener('change', function () {
      updateAllRadioGroups();
    });
  });

  // Apply styles for pre-selected items on page load
  updateAllRadioGroups();
});
