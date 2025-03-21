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
    const years = Array.from(new Set(
      publications.map((pub) => {
        const date = new Date(pub.publication_year);
        return isNaN(date.getFullYear()) ? pub.publication_year : date.getFullYear(); 
      })
    )).sort((a, b) => b - a);
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
    const publicationYear = isNaN(new Date(pub.publication_year).getFullYear()) 
      ? pub.publication_year 
      : new Date(pub.publication_year).getFullYear();
    const matchesYear = yearFilter
      ? publicationYear === parseInt(yearFilter, 10)
      : true;
    
    const matchesAuthor = authorFilter
      ? Array.isArray(pub.authors)  // Check if authors field is an array
        ? pub.authors.some(author => author.toLowerCase().includes(authorFilter.toLowerCase()))
        : pub.authors.toLowerCase().includes(authorFilter.toLowerCase())  // If it's a string
      : true;

    return matchesYear && matchesAuthor;
  })
  .sort((a, b) => {
    const yearA = new Date(a.publication_year).getFullYear();
    const yearB = new Date(b.publication_year).getFullYear();
    return yearB - yearA;
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
      <div className="publication-header">
      <div className='publication_title'>Publications</div>
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
      </div>
      <div className="publication-list">
        {paginatedPublications.map((pub) => (
          <div key={pub.paper_id} className="publication-item">
           <a href={pub.publication_link} target="_blank" rel="noopener noreferrer" className='pub_item_link'>
            <div className="pub_item_title">{pub.title}</div>
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
                <p><strong>Year:</strong> {isNaN(new Date(pub.publication_year).getFullYear()) 
                    ? pub.publication_year 
                    : new Date(pub.publication_year).getFullYear()}</p>
                  <p className="description">{pub.description}</p>
                <div className='links'>
                  {pub.git_link&&(<a href={pub.git_link} target="_blank" rel="noopener noreferrer" className="git">Git</a>)}
                  {pub.presentation_link&&<a href={pub.presentation_link} target="_blank" rel="noopener noreferrer" className="git">Presentation</a>}
                </div>
              </div>
            </div>
            </a>
          </div>
        ))}
      </div>
      <div className="pagination">
        <button className = "pagination-buttons" onClick={handlePrevPage} disabled={currentPage === 1}>
          Previous
        </button>
        <span>
          Page {currentPage} of {totalPages}
        </span>
        <button className = "pagination-buttons" onClick={handleNextPage} disabled={currentPage === totalPages}>
          Next
        </button>
      </div>
    </div>
  );
};

export default PublicationPage;

