import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import InfluencersPage from './pages/InfluencersPage';
import AuthPage from './pages/AuthPage';
// import ProjectsPage from '../pages/ProjectsPage';
// import WebPropertiesPage from '../pages/WebPropertiesPage';

const PrivateRoute = ({ children }) => {
  const isAuthenticated = !!getApiToken();
  return isAuthenticated ? children : <Navigate to="/auth" replace />;
};

const AppRouter = () => {
  return (
    <Router>
      <div>
        <nav className="bg-gray-800 p-4">
          <ul className="flex space-x-4">
            <li>
              <Link to="/" className="text-white hover:text-gray-300">Home</Link>
            </li>
            <li>
              <Link to="/influencers" className="text-white hover:text-gray-300">Influencers</Link>
            </li>
            {/* <li>
              <Link to="/projects" className="text-white hover:text-gray-300">Projects</Link>
            </li>
            <li>
              <Link to="/web-properties" className="text-white hover:text-gray-300">Web Properties</Link>
            </li> */}
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<InfluencersPage />} />
          <Route path="/influencers" element={<InfluencersPage />} />
          {/* <Route path="/projects" element={<ProjectsPage />} />
          <Route path="/web-properties" element={<WebPropertiesPage />} /> */}
          <Route path="/auth" element={<AuthPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default AppRouter;