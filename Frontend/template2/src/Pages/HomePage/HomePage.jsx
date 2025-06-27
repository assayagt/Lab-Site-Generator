import React, { useState, useEffect } from "react";
import { Container, Row, Col, Card } from 'react-bootstrap';
import { getToken } from "../../services/websiteService";
import AboutUs from "../../Components/AboutUs/AboutUs";
import "./HomePage.css";

const HomePage = () => {
  const [token, setToken] = useState("");
  const [hasAboutUs, setHasAboutUs] = useState(false);
  const [hasImage, setHasImage] = useState(false);

  useEffect(() => {
    const fetchToken = async () => {
      try {
        const domain = sessionStorage.getItem("domain");
        const fetchedToken = await getToken(domain);
        setToken(fetchedToken);
      } catch (error) {
        console.error("Error fetching token:", error);
      }
    };

    fetchToken();
  }, []);

  return (
    <Container fluid className="home-page py-5">
      <Container>
        <Row className="mb-4">
          <Col>
            <h1 className="welcome-title">Welcome to Our Lab</h1>
          </Col>
        </Row>

        <Row className="g-4">
          {/* About Us Section */}
          {hasAboutUs && (
            <Col lg={5} className="about-us-col">
              <Card className="hover-card h-100">
                <Card.Body>
                  <AboutUs />
                </Card.Body>
              </Card>
            </Col>
          )}

          {/* Image Section */}
          {hasImage && (
            <Col lg={hasAboutUs ? 7 : 12}>
              <Card className="image-card hover-card h-100">
                <Card.Img
                  variant="top"
                  src={token}
                  alt="Lab Image"
                  className="home-image"
                />
              </Card>
            </Col>
          )}
        </Row>
      </Container>
    </Container>
  );
};

export default HomePage;
