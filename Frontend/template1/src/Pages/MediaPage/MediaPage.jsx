import React, { useState, useEffect } from "react";
import "./MediaPage.css";

import { fetchGalleryImages } from "../../services/websiteService";

const MediaPage = () => {
  const [images, setImages] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null); // NEW: For modal

  const sampleImages = [
    {
      id: 1,
      url: "https://picsum.photos/seed/lab-microscope/600/400",
      alt: "Close-up of a microscope in the lab",
    },
    {
      id: 2,
      url: "https://picsum.photos/seed/team-meeting/600/400",
      alt: "Research team meeting around a table",
    },
    {
      id: 3,
      url: "https://picsum.photos/seed/chemical-bottles/600/400",
      alt: "Reagent bottles on a shelf",
    },
    {
      id: 4,
      url: "https://picsum.photos/seed/dna-analysis/600/400",
      alt: "DNA gel electrophoresis under UV light",
    },
    {
      id: 5,
      url: "https://picsum.photos/seed/robot-prototype/600/400",
      alt: "Lab robot prototype on the bench",
    },
    {
      id: 6,
      url: "https://picsum.photos/seed/conference-poster/600/400",
      alt: "Researcher presenting a conference poster",
    },
    {
      id: 7,
      url: "https://picsum.photos/seed/drone-testing/600/400",
      alt: "Outdoor drone testing session",
    },
    {
      id: 8,
      url: "https://picsum.photos/seed/soldering-station/600/400",
      alt: "Electronics soldering station close-up",
    },
  ];
  useEffect(() => {
    const loadGallery = async () => {
      const domain = sessionStorage.getItem("domain");
      if (!domain) return;

      const data = await fetchGalleryImages(domain);
      console.log(data);
      if (Array.isArray(data)) {
        const images = data.map((item, index) => ({
          id: index,
          url: item.data_url, // ✅ use the base64 data directly
          alt: item.filename,
        }));
        setImages(images);
      } else {
        console.error(data);
      }
    };

    loadGallery();
  }, []);

  return (
    <div className="gallery-page">
      <h2 className="gallery_title">Media Gallery</h2>

      <div className="gallery_grid">
        {images.length ? (
          images.map((img) => (
            <div key={img.id} className="gallery_item">
              <img
                src={img.url}
                alt={img.alt || "media"}
                className="image"
                onClick={() => setSelectedImage(img)}
              />
            </div>
          ))
        ) : (
          <p className="gallery_empty">No images uploaded yet.</p>
        )}
      </div>
      {selectedImage && (
        <div className="image_modal" onClick={() => setSelectedImage(null)}>
          <div className="modal_content" onClick={(e) => e.stopPropagation()}>
            <button
              className="close_button"
              onClick={() => setSelectedImage(null)}
            >
              ×
            </button>
            <img
              src={selectedImage.url}
              alt={selectedImage.alt}
              className="modal_image"
            />
          </div>
        </div>
      )}
    </div>
  );
};
export default MediaPage;
