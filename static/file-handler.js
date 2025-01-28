document.addEventListener('DOMContentLoaded', () => {
    const MAX_FILES = 5;
    const MAX_FILE_SIZE_MB = 100;
    const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;

    // Общие элементы
    const fileDropZone = document.getElementById('fileDropZone');
    const fileInput = document.getElementById('fileInput');
    const fileList = document.getElementById('fileList');
    const actionPanel = document.getElementById('actionPanel');
    const convertButton = document.getElementById('convertButton');
    const uploadForm = document.getElementById('uploadForm');

    const selectedFiles = new DataTransfer();

    if (!fileDropZone || !fileInput || !fileList || !actionPanel || !convertButton || !uploadForm) {
        console.error('One or more required elements are missing.');
        return;
    }

    const allowedExtensions = fileInput.getAttribute('data-allowed-extensions')?.split(',') || [];
    if (allowedExtensions.length === 0) {
        console.error('Allowed extensions are not defined in the fileInput element.');
        return;
    }

    fileDropZone.addEventListener('click', () => {
        fileInput.click();
    });

    fileDropZone.addEventListener('dragover', (event) => {
        event.preventDefault();
        fileDropZone.classList.add('dragover');
    });

    fileDropZone.addEventListener('dragleave', () => {
        fileDropZone.classList.remove('dragover');
    });

    fileDropZone.addEventListener('drop', (event) => {
        event.preventDefault();
        fileDropZone.classList.remove('dragover');
        handleFiles(event.dataTransfer.files);
    });

    fileInput.addEventListener('change', () => {
        handleFiles(fileInput.files);
        actionPanel.style.display = 'flex';
    });

    function handleFiles(files) {
        if (selectedFiles.items.length + files.length > MAX_FILES) {
            alert(`Нельзя загружать больше ${MAX_FILES} файлов одновременно.`);
            return;
        }

        Array.from(files).forEach((file) => {
            if (!isAllowedExtension(file.name)) {
                alert(`Формат файла "${file.name}" не поддерживается. Разрешены: ${allowedExtensions.join(', ')}`);
                return;
            }

            if (file.size > MAX_FILE_SIZE_BYTES) {
                alert(`Файл "${file.name}" превышает максимальный размер ${MAX_FILE_SIZE_MB} МБ.`);
                return;
            }

            if (!isFileAlreadyListed(file.name)) {
                selectedFiles.items.add(file);
                const li = document.createElement('li');
                li.className = 'file-item';

                const removeButton = document.createElement('button');
                removeButton.textContent = '✖';
                removeButton.className = 'remove-file-button';
                removeButton.addEventListener('click', () => {
                    removeFile(file.name);
                    li.remove();
                });
                li.appendChild(removeButton);

                const span = document.createElement('span');
                span.textContent = file.name;
                li.appendChild(span);

                fileList.appendChild(li);
            }
        });

        fileInput.files = selectedFiles.files;
        convertButton.style.display = fileList.children.length > 0 ? 'block' : 'none';
    }

    function isAllowedExtension(fileName) {
        return allowedExtensions.some((ext) => fileName.toLowerCase().endsWith(ext.trim()));
    }

    function isFileAlreadyListed(fileName) {
        return Array.from(fileList.children).some((li) => li.querySelector('span').textContent === fileName);
    }

    function removeFile(fileName) {
        for (let i = 0; i < selectedFiles.items.length; i++) {
            if (selectedFiles.items[i].getAsFile().name === fileName) {
                selectedFiles.items.remove(i);
                break;
            }
        }
        fileInput.files = selectedFiles.files;
        convertButton.style.display = fileList.children.length > 0 ? 'block' : 'none';
    }

    convertButton.addEventListener('click', (event) => {
        if (fileList.children.length === 0) {
            alert('Пожалуйста, выберите файлы перед конвертацией.');
            event.preventDefault();
        } else {
            uploadForm.submit();
        }
    });

    document.addEventListener('DOMContentLoaded', () => {
        const testIcons = document.querySelectorAll('.test-feature-icon');
    
        testIcons.forEach((icon) => {
            icon.addEventListener('mouseenter', () => {
                icon.classList.add('tooltip-visible');
            });
    
            icon.addEventListener('mouseleave', () => {
                icon.classList.remove('tooltip-visible');
            });
        });
    });
});
