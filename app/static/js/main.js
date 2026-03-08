// FreshVision AI — main.js
// Drag-and-drop upload + file preview

(function () {
  const dropZone   = document.getElementById('drop-zone');
  const fileInput  = document.getElementById('file-input');
  const previewBox = document.getElementById('preview-box');
  const dropDef    = document.getElementById('drop-default');
  const previewImg = document.getElementById('preview-img');
  const fileLabel  = document.getElementById('file-name');
  const submitBtn  = document.getElementById('submit-btn');

  if (!dropZone) return;

  // File input change
  fileInput.addEventListener('change', function () {
    if (this.files && this.files[0]) showPreview(this.files[0]);
  });

  // Drag events
  ['dragenter', 'dragover'].forEach(evt =>
    dropZone.addEventListener(evt, e => {
      e.preventDefault();
      dropZone.classList.add('dragover');
    })
  );

  ['dragleave', 'drop'].forEach(evt =>
    dropZone.addEventListener(evt, e => {
      e.preventDefault();
      dropZone.classList.remove('dragover');
    })
  );

  dropZone.addEventListener('drop', function (e) {
    const file = e.dataTransfer.files[0];
    if (!file) return;
    // Inject into file input via DataTransfer
    const dt = new DataTransfer();
    dt.items.add(file);
    fileInput.files = dt.files;
    showPreview(file);
  });

  function showPreview(file) {
    const allowed = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
    if (!allowed.includes(file.type)) {
      alert('Please upload a JPG, PNG, or WEBP image.');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      alert('File too large. Maximum size is 10MB.');
      return;
    }
    const reader = new FileReader();
    reader.onload = function (e) {
      previewImg.src = e.target.result;
      if (fileLabel) fileLabel.textContent = file.name;
      previewBox.style.display = 'block';
      dropDef.style.display = 'none';
    };
    reader.readAsDataURL(file);
  }

  // Show loading state on submit
  const form = document.getElementById('upload-form');
  if (form && submitBtn) {
    form.addEventListener('submit', function () {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Classifying...';
    });
  }
})();
