import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./MyAccountPage.css";
import {
  getCustomWebsites,
  getCustomSite,
  deleteWebsite,
} from "../../services/MyAccount";
import { useWebsite } from "../../Context/WebsiteContext";

const MyAccountPage = () => {
  const [websites, setWebsites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const { setWebsite } = useWebsite();
  const handleStartNewWebsite = () => {
    setWebsite({
      domain: "",
      websiteName: "",
      components: [],
      template: "",
      created: false,
      generated: false,
      about_us: "",
      contact_us: {
        address: "",
        email: "",
        phone_num: "",
      },
      gallery: [], // Add gallery array here
    });
    navigate("/choose-components"); // Redirect user to start website creation
  };
  useEffect(() => {
    const fetchWebsites = async () => {
      try {
        const data = await getCustomWebsites(sessionStorage.getItem("sid"));
        if (data.response === "false") {
          throw new Error("Failed to fetch websites");
        }
        const websitesArray = Object.entries(data.websites || {}).map(
          ([domain, details]) => ({
            domain,
            ...details,
          })
        );
        setWebsites(websitesArray);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchWebsites();
  }, []);

  const handleWebsiteClick = async (websiteDomain) => {
    const selectedWebsite = websites.find(
      (site) => site.domain === websiteDomain
    );
    const data = await getCustomSite(
      sessionStorage.getItem("sid"),
      websiteDomain
    );
    setWebsite({
      components: data?.data?.components || [],
      template: data?.data?.template || "",
      domain: data.data.domain || "",
      websiteName: data.data.name || "",
      created: true,
      generated: selectedWebsite.generated || false,
      about_us: data?.data?.about_us || "",
      contact_us: data?.data?.contact_us || {
        address: "",
        email: "",
        phone_num: "",
      },
      gallery: data?.data?.gallery_images || [], // Add gallery array here
    });

    navigate("/choose-components");
  };

  const handleDeleteWebsite = async (domainToDelete) => {
    const confirmed = window.confirm(
      `Are you sure you want to delete the website "${domainToDelete}"? This cannot be undone.`
    );
    if (!confirmed) return;

    try {
      const response = await deleteWebsite(
        sessionStorage.getItem("sid"),
        domainToDelete
      );
      if (response?.response === "true") {
        // Filter out the deleted website from the list
        setWebsites((prevWebsites) =>
          prevWebsites.filter((site) => site.domain !== domainToDelete)
        );
      } else {
        setError("Failed to delete website: " + response?.message);
      }
    } catch (err) {
      setError("An error occurred while deleting the website.");
      console.error(err);
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="myAccountPage">
      <h2>My Account</h2>
      <div className="myWebsites">
        <h3>Your Websites</h3>
        {websites?.length > 0 ? (
          <div className="websiteList">
            {websites.map((website, index) => (
              <div
                key={index}
                className="websiteItem"
                onClick={() => handleWebsiteClick(website.domain)}
              >
                <div>{website.site_name}</div>
                <div>{website.domain}</div>
                <div className={website.generated ? "" : "notGenerated"}>
                  {website.generated ? "Generated" : "Not Generated"}
                </div>

                <button
                  className="delete-button"
                  onClick={(e) => {
                    e.stopPropagation(); // prevent triggering website load
                    handleDeleteWebsite(website.domain);
                  }}
                  title="Remove participant"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">
                    <path
                      fill="currentColor"
                      d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"
                    />
                    <path
                      fill="currentColor"
                      d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"
                    />
                  </svg>
                </button>
              </div>
            ))}
          </div>
        ) : (
          <p>No websites available.</p>
        )}
      </div>
      {/* Start New Website Button */}
      <div className="newWebsiteContainer">
        <button className="newWebsiteButton" onClick={handleStartNewWebsite}>
          + Start New Website
        </button>
      </div>
    </div>
  );
};

export default MyAccountPage;
