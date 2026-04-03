import React, { useEffect, useRef, useState } from 'react'
import './UploadFiles.css'
const UploadFiles = () => {

  const [files, setFiles] = useState([]);
  const inputRef = useRef(null);

  useEffect(() => {
    if(inputRef.current){
      inputRef.current.setAttribute('webkitdirectory', '');
      inputRef.current.setAttribute('directory', '');
    }
  }, []);

  const handleChange = (e) => {
    setFiles(Array.from(e.target.files));
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    if(files.length === 0 ){
      alert("Please select Files");
      return;
    }

    const formData = new FormData();
  
    files.forEach((file) => {
      formData.append("documents", file);
    });
  
    try {
      const res = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      console.log(data);
    } catch (error) {
      console.error(error);
    }
  }


  return (
    <div className='uploadFiles'>
      <form onSubmit={handleSubmit}>
        <input type="file" multiple ref={inputRef} name="upload-file" onChange={handleChange} />
        <button type="submit">Upload</button>
      </form>
    </div>
  )
}

export default UploadFiles
