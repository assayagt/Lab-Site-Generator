import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import WelcomePage from './pages/WelcomePage/WelcomePage';
import ChooseComponentsPage from './pages/Generate/ChooseComponentsPage/ChooseComponentsPage';
import UploadFilesPage from './pages/Generate/UploadFilesPage/UploadFilesPage';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  return (
    <Router>
      <Switch>
        <Route exact path="/">
          <WelcomePage onLogin={handleLogin} isLoggedIn={isLoggedIn} />
        </Route>
        <Route path="/choose-components">
          {isLoggedIn ? (
            <ChooseComponentsPage />
          ) : (
            <Redirect to="/" />
          )}
        </Route>
        <Route path="/upload-files">
          {isLoggedIn ? (
            <UploadFilesPage />
          ) : (
            <Redirect to="/" />
          )}
        </Route>
       
      </Switch>
    </Router>
  );
}

export default App;
