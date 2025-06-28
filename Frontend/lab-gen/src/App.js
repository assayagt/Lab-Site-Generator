import { BrowserRouter as Router, Route, Routes } from "react-router-dom"; // Import Routes, Navigate
import WelcomePage from "./pages/WelcomePage/WelcomePage";
import ChooseComponentsPage from "./pages/Generate/ChooseComponentsPage/ChooseComponentsPage";
import { AuthProvider } from "./Context/AuthContext";
import { WebsiteProvider } from "./Context/WebsiteContext";
import MyAccountPage from "./pages/MyAccountPage/MyAccountPage";
import Header from "./components/Header/Header";
import { GoogleOAuthProvider } from "@react-oauth/google";

function App() {
  return (
    <GoogleOAuthProvider clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID}>
      <AuthProvider>
        <WebsiteProvider>
          <Router>
            <Header title="LabLauncher" />
            <Routes>
              <Route path="/" element={<WelcomePage />} />
              <Route
                path="/choose-components"
                element={<ChooseComponentsPage />}
              />
              <Route path="/my-account" element={<MyAccountPage />} />
            </Routes>
          </Router>
        </WebsiteProvider>
      </AuthProvider>
    </GoogleOAuthProvider>
  );
}

export default App;
