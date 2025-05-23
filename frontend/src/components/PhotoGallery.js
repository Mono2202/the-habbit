import { React, useEffect } from "react";
import "./PhotoGallery.css";
import { PICTURES } from "../consts/ImageFiles";

function PhotoGallery({ level, onPhotoClick }) {
  const filteredPics = PICTURES.filter((pic) => {
    const levelNumber = parseInt(pic.split("_")[0].split("/").at(-1));
    return levelNumber <= level;
  });

  const lastPic = filteredPics.pop();

  useEffect(() => {
    const timeout = setTimeout(() => {
      window.dispatchEvent(new Event('resize'));
    }, 300);
    return () => clearTimeout(timeout);
  }, []);

  return (
    <div className="gallery-container">
      <h2 className="gallery-title">Gallery</h2>
      <div className="gallery-grid">
        {filteredPics.map((src, index) => (
          <div className="gallery-item" key={index}>
            <img src={src} onClick={() => onPhotoClick(src)} alt={lastPic} />
          </div>
        ))}
        <div className="gallery-item hidden-gallery-item">
          <img
            src={lastPic}
            onClick={() => onPhotoClick(lastPic)}
            alt={lastPic}
          />
        </div>
      </div>
    </div>
  );
}

export default PhotoGallery;
