import React, { useState, useEffect } from "react";
import { useEditMode } from "../../Context/EditModeContext";
import { Plus, Save, X, ChevronDown, ChevronUp } from "lucide-react";
import { addNewsRecord } from "../../services/websiteService";
import "./News.css";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const NewsSection = (props) => {
  const { editMode } = useEditMode();

  const [timelineData, setTimelineData] = useState([]);
  const [showAllNews, setShowAllNews] = useState(false);
  const [itemsToShow] = useState(3); // Show only 3 items initially

  const [newItem, setNewItem] = useState({
    date: "",
    link: "",
    text: "",
  });
  const [showAddForm, setShowAddForm] = useState(false);

  // Sort news by date (newest first) when props.info changes
  useEffect(() => {
    if (props.info && props.info.length > 0) {
      const sortedData = [...props.info].sort((a, b) => {
        const dateA = new Date(a.date);
        const dateB = new Date(b.date);
        return dateB - dateA; // Newest first
      });
      setTimelineData(sortedData);
    } else {
      setTimelineData([]);
    }
  }, [props.info]);

  const handleAddItem = async () => {
    const userId = sessionStorage.getItem("sid");
    const domain = props.domain;

    if (newItem.date && newItem.link && newItem.description) {
      const isoDate = newItem.date.toISOString().replace("Z", "");

      const response = await addNewsRecord(
        userId,
        domain,
        newItem.description,
        newItem.link,
        isoDate
      );

      if (response?.response === "true") {
        const newTimelineItem = {
          id: Date.now(),
          date: newItem.date,
          link: newItem.link,
          text: newItem.description,
        };

        // Add new item and re-sort the array
        const updatedData = [newTimelineItem, ...timelineData].sort((a, b) => {
          const dateA = new Date(a.date);
          const dateB = new Date(b.date);
          return dateB - dateA; // Newest first
        });

        setTimelineData(updatedData);
        setNewItem({ date: "", link: "", text: "" });
        setShowAddForm(false);
      } else {
        console.error("Failed to add news:", response?.message);
      }
    }
  };

  // Get the items to display based on showAllNews state
  const displayedItems = showAllNews
    ? timelineData
    : timelineData.slice(0, itemsToShow);
  const hasMoreItems = timelineData.length > itemsToShow;

  return (
    <div className="timeline-container">
      <div className="timeline-header">
        {/* <h2 className="timeline-title">News</h2> */}

        {editMode && (
          <>
            {!showAddForm ? (
              <button
                className="add-button"
                onClick={() => setShowAddForm(true)}
              >
                <Plus size={16} />
                Add News
              </button>
            ) : (
              <div
                className="popup-overlay"
                onClick={() => setShowAddForm(false)}
              >
                <div
                  className="popup-content-news"
                  onClick={(e) => e.stopPropagation()}
                >
                  <h3>Add New News Item</h3>
                  <div className="form-group">
                    <label className="form-label">Date/Year:</label>
                    <DatePicker
                      selected={newItem.date}
                      onChange={(date) => setNewItem({ ...newItem, date })}
                      dateFormat="yyyy-MM-dd"
                      className="form-input"
                      placeholderText="Select a date"
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Link:</label>
                    <input
                      type="text"
                      className="form-input"
                      value={newItem.link}
                      onChange={(e) =>
                        setNewItem({ ...newItem, link: e.target.value })
                      }
                      placeholder="Timeline event title"
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Description:</label>
                    <textarea
                      className="form-textarea"
                      value={newItem.description}
                      onChange={(e) =>
                        setNewItem({ ...newItem, description: e.target.value })
                      }
                      placeholder="Describe what happened..."
                    />
                  </div>
                  <div className="form-buttons">
                    <button className="save-button" onClick={handleAddItem}>
                      <Save size={14} />
                      Add Item
                    </button>
                    <button
                      className="cancel-button"
                      onClick={() => {
                        setShowAddForm(false);
                        setNewItem({ date: "", link: "", description: "" });
                      }}
                    >
                      <X size={14} />
                      Cancel
                    </button>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {timelineData.length === 0 && <div> No News</div>}

      {timelineData.length > 0 && (
        <>
          <div className="timeline">
            <div className="timeline-line"></div>

            {displayedItems.map((item, index) => (
              <div key={item.id} className="timeline-item">
                <div className="timeline-point"></div>

                <div className="timeline-content">
                  <div className="timeline-date">
                    {new Date(item.date).toLocaleDateString("en-GB", {
                      year: "numeric",
                      month: "short",
                      day: "numeric",
                    })}
                  </div>
                  <div className="timeline-content-wrapper">
                    <a
                      href={item.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="timeline-description-link"
                    >
                      <p className="timeline-description">{item.text}</p>
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* See More / See Less Button */}
          {hasMoreItems && (
            <div className="see-more-container">
              <button
                className="see-more-button"
                onClick={() => setShowAllNews(!showAllNews)}
              >
                {showAllNews ? (
                  <>
                    <ChevronUp size={16} />
                    See Less
                  </>
                ) : (
                  <>
                    <ChevronDown size={16} />
                    See More ({timelineData.length - itemsToShow} more)
                  </>
                )}
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default NewsSection;
