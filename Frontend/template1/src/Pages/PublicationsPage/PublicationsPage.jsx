import React, { useState, useEffect } from 'react';
import './PublicationsPage.css';
import { getApprovedPublications } from '../../services/websiteService';
const PublicationPage = () => {
  const [publications, setPublications] = useState([]);
  const [yearFilter, setYearFilter] = useState('');
  const [authorFilter, setAuthorFilter] = useState('');
  const [availableYears, setAvailableYears] = useState([]);
  const [availableAuthors, setAvailableAuthors] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;


  useEffect(() => {
    const fetchPublications = async () => {
      try {
        const domain = sessionStorage.getItem('domain');
        const fetchedPublications = await getApprovedPublications(domain);
        setPublications(fetchedPublications || []);
      } catch (error) {
        console.error('Error fetching publications:', error);
      } finally {
        
      }
    };

    fetchPublications();
  }, []);

  useEffect(() => {
    const years = Array.from(new Set(publications.map((pub) => {
      // Ensure to extract only the year if it's a full date
      const year = new Date(pub.publication_year).getFullYear();
      return year;
    }))).sort((a, b) => b - a); // Sort in descending order
    setAvailableYears(years);

    const authors = Array.from(
      new Set(publications.flatMap((pub) => pub.authors || []))
    ).sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' }));
    setAvailableAuthors(authors);
  }, [publications]);

  const handleYearChange = (event) => {
    setYearFilter(event.target.value);
    setCurrentPage(1); // Reset to first page
  };

  const handleAuthorChange = (event) => {
    setAuthorFilter(event.target.value);
    setCurrentPage(1); // Reset to first page
  };

  const filteredPublications = publications
  .filter((pub) => {
    const publicationYear = new Date(pub.publication_year).getFullYear(); // Extract the year from the full date
    const matchesYear = yearFilter
      ? publicationYear === parseInt(yearFilter, 10) // Compare the extracted year with the yearFilter
      : true;
    const matchesAuthor = authorFilter
      ? typeof pub.authors === 'string' && pub.authors.toLowerCase().includes(authorFilter.toLowerCase())
      : true;
    return matchesYear && matchesAuthor;
  })
  .sort((a, b) => {
    const yearA = new Date(a.publication_year).getFullYear();
    const yearB = new Date(b.publication_year).getFullYear();
    return yearB - yearA; // Sort based on the extracted year
  });

  const paginatedPublications = filteredPublications.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const totalPages = Math.ceil(filteredPublications.length / itemsPerPage);

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  return (
    <div className="publication-page">
      <h1>Publications</h1>
      <div className="filters">
        <label className='specific-filter'>
          Filter by Year:
          <select className='allOptions' value={yearFilter} onChange={handleYearChange}>
            <option value="">All Years</option>
            {availableYears.map((year) => (
              <option key={year} value={year}>
                {year}
              </option>
            ))}
          </select>
        </label>
        <label className='specific-filter'>
          Filter by Author:
          <select className='allOptions' value={authorFilter} onChange={handleAuthorChange}>
            <option value="">All Authors</option>
            {availableAuthors.map((author) => (
              <option key={author} value={author}>
                {author}
              </option>
            ))}
          </select>
        </label>
      </div>
      <div className="publication-list">
        {paginatedPublications.map((pub) => (
          <div key={pub.paper_id} className="publication-item">
            <h2>{pub.title}</h2>
            <div className="publication-item-info">
              {pub.video && (
                <iframe
                  className="video"
                  src={pub.video}
                  title={pub.title}
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                ></iframe>
              )}
              <div>
                <p><strong>Authors:</strong> {pub.authors.join(', ') || "Unknown Authors"}</p>
                <p><strong>Year:</strong> {pub.publication_year}</p>
                <p className="description">{pub.description}</p>
                <div className='links'>
                  {pub.git&&(<div className="git">Git</div>)}
                  {pub.presentation_link&&<div className="presentation">Presentation</div>}
                  <a href={pub.publication_link} target="_blank" rel="noopener noreferrer">Read More</a>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="pagination">
        <button onClick={handlePrevPage} disabled={currentPage === 1}>
          Previous
        </button>
        <span>
          Page {currentPage} of {totalPages}
        </span>
        <button onClick={handleNextPage} disabled={currentPage === totalPages}>
          Next
        </button>
      </div>
    </div>
  );
};

export default PublicationPage;

