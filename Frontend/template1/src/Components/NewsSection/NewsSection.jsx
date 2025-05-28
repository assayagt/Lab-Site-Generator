import React, { useState } from "react";
import { useEditMode } from "../../Context/EditModeContext";
import { Plus, Edit3, Save, X } from "lucide-react";
import "./News.css";

const NewsSection = () => {
  const { editMode } = useEditMode();

  const [timelineData, setTimelineData] = useState([
    {
      id: 1,
      date: "2024",
      link: "Started New Project",
      description:
        "Launched the initial phase of our development project with a focus on user experience.",
    },
    {
      id: 2,
      date: "2024",
      link: "Team Expansion",
      description:
        "Grew our team from 5 to 15 members, bringing in specialists from various fields.",
    },
    {
      id: 3,
      date: "2022",
      link: "First Product Launch",
      description:
        "Successfully launched our first product to market with positive user feedback.",
    },
    {
      id: 4,
      date: "2021",
      link: "Company Founded",
      description:
        "Established the company with a vision to create innovative solutions.",
    },
  ]);

  const [newItem, setNewItem] = useState({
    date: "",
    link: "",
    description: "",
  });
  const [showAddForm, setShowAddForm] = useState(false);

  const handleAddItem = () => {
    if (newItem.date && newItem.title && newItem.description) {
      const newTimelineItem = {
        id: Date.now(),
        ...newItem,
      };
      setTimelineData([newTimelineItem, ...timelineData]);
      setNewItem({ date: "", link: "", description: "" });
      setShowAddForm(false);
    }
  };

  const handleDeleteItem = (id) => {
    setTimelineData(timelineData.filter((item) => item.id !== id));
  };

  return (
    <div className="timeline-container">
      <div className="timeline-header">
        <h2 className="timeline-title">News</h2>
        {editMode && (
          <>
            {!showAddForm ? (
              <button
                className="add-button"
                onClick={() => setShowAddForm(true)}
              >
                <Plus size={16} />
                Add New Timeline Item
              </button>
            ) : (
              <div className="add-form">
                <div className="form-group">
                  <label className="form-label">Date/Year</label>
                  <input
                    type="text"
                    className="form-input"
                    value={newItem.date}
                    onChange={(e) =>
                      setNewItem({ ...newItem, date: e.target.value })
                    }
                    placeholder="e.g., 2025"
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Link</label>
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
                  <label className="form-label">Description</label>
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
            )}
          </>
        )}
      </div>

      <div className="timeline">
        <div className="timeline-line"></div>

        {timelineData.map((item, index) => (
          <div key={item.id} className="timeline-item">
            <div className="timeline-point"></div>

            <div className="timeline-content">
              <div className="timeline-date">{item.date}</div>
              <h3 className="timeline-title-text">{item.link}</h3>
              <p className="timeline-description">{item.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default NewsSection;
