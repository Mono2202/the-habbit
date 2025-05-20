import React from 'react';
import './PhotoGallery.css';
import { PICTURES } from '../consts/ImageFiles';

function PhotoGallery({level}) {

  const filteredPics = PICTURES.filter(pic => {
    const levelNumber = parseInt(pic.split('_')[0].split('/').at(-1));
    return levelNumber < level;
  });

  return (
    <div className="gallery-container">
      <h2 className="gallery-title">Gallery</h2>
      <div className="gallery-grid">
        {filteredPics.map((src, index) => (
          <div className="gallery-item" key={index}>
            <img src={src} loading="lazy" />
          </div>
        ))}
      </div>
    </div>
  );
};

export default PhotoGallery;
