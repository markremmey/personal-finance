import React, { useState } from 'react';

function FileUploadComponent({ onFileUploadSuccess }) {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    console.log('Handling File Change...')
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    console.log('Uploading file...')
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
      console.log('formData', formData)

      try {
        const response = await fetch('http://localhost:5000/upload_to_blob', {
          method: 'POST',
          body: formData
          // headers: {
          //   'Content-Type': 'application/json'
          // },
           // JSON.stringify({
          //   "file": "TEST BLOB"
          // }) // formData,
        });

        if (response.ok) {
          alert('File uploaded successfully');
          onFileUploadSuccess();
        } else {
          alert('File upload failed');
        }
      } catch (error) {
        console.error('Error uploading file:', error);
        alert('File upload failed');
      }
    } else {
      alert('Please select a file to upload');
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
}

export default FileUploadComponent;