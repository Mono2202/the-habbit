import React from 'react';
import './PhotoGallery.css';

const photos = [
  '/assets/sprites/alakazam.png',
  '/assets/sprites/alakazam.png',
  '/assets/sprites/alakazam.png',
  '/assets/sprites/alakazam.png',
  '/assets/sprites/alakazam.png',
  '/assets/sprites/alakazam.png',
  '/assets/sprites/alakazam.png',
];

function PhotoGallery() {
  return (
    <div className="gallery-container">
      <h2 className="gallery-title">Gallery</h2>
      <div className="gallery-grid">
        {photos.map((src, index) => (
          <div className="gallery-item" key={index}>
            <img src={src} loading="lazy" />
          </div>
        ))}
      </div>
    </div>
  );
};

export default PhotoGallery;
