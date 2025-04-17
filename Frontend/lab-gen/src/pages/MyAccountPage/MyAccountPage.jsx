import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./MyAccountPage.css";
import { getCustomWebsites, getCustomSite } from "../../services/MyAccount";
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
    console.log(data);
    setWebsite({
      components: data?.data?.components || [],
      template: data?.data?.template || "",
      domain: data.data.domain || "",
      websiteName: data.data.name || "",
      created: true,
      generated: selectedWebsite.generated || false,
    });

    navigate("/choose-components");
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
                {/* <button
                  className="delete-button"
                  onClick={() => console.log("")}
                >
                  🗑️
                </button> */}
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
