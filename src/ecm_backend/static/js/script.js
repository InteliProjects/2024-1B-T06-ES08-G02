document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const form = document.getElementById('upload-form');
  
    uploadArea.addEventListener('dragover', (event) => {
      event.preventDefault();
      uploadArea.classList.add('dragover');
    });
  
    uploadArea.addEventListener('dragleave', () => {
      uploadArea.classList.remove('dragover');
    });
  
    uploadArea.addEventListener('drop', (event) => {
      event.preventDefault();
      uploadArea.classList.remove('dragover');
  
      const files = event.dataTransfer.files;
      fileInput.files = files;
  
    });
  });
  