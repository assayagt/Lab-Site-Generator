import React, { useRef } from "react";

const FeatureCarousel = ({ features }) => {
  const carouselRef = useRef(null);

  const handleMouseEnter = (direction) => {
    if (carouselRef.current) {
      const scrollAmount = direction === "right" ? 300 : -300;  // Amount to scroll
      carouselRef.current.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
  };

  return (
    <div className="feature-carousel-container">
      <div
        className="feature-carousel"
        ref={carouselRef}
        onMouseEnter={() => handleMouseEnter("left")}
        onMouseLeave={() => handleMouseEnter("right")}
      >
        {features.map((feature, index) => (
          <div key={index} className="feature-card">
            {feature}
          </div>
        ))}
      </div>
    </div>
  );
};

export default FeatureCarousel;
