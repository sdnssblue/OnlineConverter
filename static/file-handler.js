document.addEventListener('DOMContentLoaded', () => {
    // Общие элементы
    const fileDropZone = document.getElementById('fileDropZone');
    const fileInput = document.getElementById('fileInput');
    const fileList = document.getElementById('fileList');
    const actionPanel = document.getElementById('actionPanel');
    const convertButton = document.getElementById('convertButton');
    const uploadForm = document.getElementById('uploadForm');

    const selectedFiles = new DataTransfer();

    // Проверяем, чтобы все элементы были найдены
    if (!fileDropZone || !fileInput || !fileList || !actionPanel || !convertButton || !uploadForm) {
        console.error('One or more required elements are missing.');
        return;
    }

    // Чтение разрешённых расширений из атрибута
    const allowedExtensions = fileInput.getAttribute('data-allowed-extensions')?.split(',') || [];
    if (allowedExtensions.length === 0) {
        console.error('Allowed extensions are not defined in the fileInput element.');
        return;
    }

    // Открытие файлового окна по клику на область загрузки
    fileDropZone.addEventListener('click', () => {
        fileInput.click();
    });

    // Drag-and-drop события
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

    // Обработчик выбора файлов
    fileInput.addEventListener('change', () => {
        handleFiles(fileInput.files);
        actionPanel.style.display = 'flex';
    });

    // Обработка загруженных файлов
    function handleFiles(files) {
        Array.from(files).forEach((file) => {
            if (isAllowedExtension(file.name)) {
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
            } else {
                alert(`Формат файла "${file.name}" не поддерживается. Разрешены: ${allowedExtensions.join(', ')}`);
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
});
