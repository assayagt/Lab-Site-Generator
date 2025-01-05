import React, { useState, useEffect } from 'react';
import './PublicationsPage.css';

const PublicationPage = ({ publications }) => {
  const [yearFilter, setYearFilter] = useState('');
  const [authorFilter, setAuthorFilter] = useState('');
  const [availableYears, setAvailableYears] = useState([]);
  const [availableAuthors, setAvailableAuthors] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  useEffect(() => {
    const years = Array.from(new Set(publications.map((pub) => pub.publication_year)));
    setAvailableYears(years);

    const authors = Array.from(
      new Set(publications.flatMap((pub) => pub.authors.split(', ').map((author) => author.trim())))
    );
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

  const filteredPublications = publications.filter((pub) => {
    const matchesYear = yearFilter ? pub.publication_year.toString() === yearFilter : true;
    const matchesAuthor = authorFilter
      ? pub.authors.toLowerCase().includes(authorFilter.toLowerCase())
      : true;
    return matchesYear && matchesAuthor;
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
        <label>
          Filter by Year:
          <select value={yearFilter} onChange={handleYearChange}>
            <option value="">All Years</option>
            {availableYears.map((year) => (
              <option key={year} value={year}>
                {year}
              </option>
            ))}
          </select>
        </label>
        <label>
          Filter by Author:
          <select value={authorFilter} onChange={handleAuthorChange}>
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
            <div className = "publication-item-info">
                <div className='video'></div>
                <div>
                    <p><strong>Authors:</strong> {pub.authors}</p>
                    <p><strong>Year:</strong> {pub.publication_year}</p>
                    <p className="description"><strong>Description:</strong> {pub.description}</p>
                    <div className='links'>
                        <div className="git">Git</div>
                        <div className="presentation">Presentation</div>
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
