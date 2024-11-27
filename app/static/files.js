async function uploadFiles() {
    const fileInput = document.getElementById('fileInput');
    const files = fileInput.files;

    if (files.length === 0) {
        alert('Please select files to upload');
        return;
    }

    if (files.length > 40) {
        alert('Maximum 40 files can be uploaded at once');
        return;
    }

    const totalSize = Array.from(files).reduce((total, file) => total + file.size, 0);
    if (totalSize > 1048576) {
        alert('Total file size cannot exceed 1MB');
        return;
    }

    try {
        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }

        const response = await uploadGroupFiles(formData);
        alert('Files uploaded successfully');
        await listGroupFiles();
        fileInput.value = '';
    } catch (error) {
        console.error('Error uploading files:', error);
    }
}

async function listGroupFiles() {
    try {
        const files = await getGroupFiles();
        const filesList = document.getElementById('filesList');
        filesList.innerHTML = '';

        if (files.length === 0) {
            filesList.innerHTML = '<p>No files uploaded</p>';
            return;
        }

        files.forEach(file => {
            const fileItem = document.createElement('div');
            fileItem.classList.add('file-item');
            fileItem.innerHTML = `
                <span>${file}</span>
                <button onclick="downloadFile('${file}')">Download</button>
            `;
            filesList.appendChild(fileItem);
        });
    } catch (error) {
        console.error('Error listing files:', error);
    }
}

async function downloadFile(filename) {
    try {
        const response = await downloadSingleFile(filename);
        const url = window.URL.createObjectURL(await response.blob());
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        console.error('Error downloading file:', error);
    }
}

async function downloadAllFiles() {
    try {
        const response = await downloadEntireGroupFiles();
        const url = window.URL.createObjectURL(await response.blob());
        const a = document.createElement('a');
        a.href = url;
        a.download = 'group_files.zip';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        console.error('Error downloading all files:', error);
    }
}

window.onload = async () => {
    await listGroupFiles();
};
