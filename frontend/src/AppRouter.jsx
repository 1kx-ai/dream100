import React, { Suspense } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import TopNavBar from './components/layout/TopNavBar';
import InfluencersPage from './pages/InfluencersPage';
import ProjectsPage from './pages/ProjectsPage';
import ProjectSelectorPage from './pages/ProjectSelectorPage';
import AuthPage from './pages/AuthPage';
import ContentsPage from './pages/ContentsPage';
import ContentView from './components/ContentView';

const PrivateRoute = ({ children }) => {
  const isAuthenticated = !!localStorage.getItem('API_TOKEN');
  const hasSelectedProject = !!localStorage.getItem('currentProjectId');

  if (!isAuthenticated) {
    return <Navigate to="/auth" replace />;
  }

  if (!hasSelectedProject) {
    return <Navigate to="/select-project" replace />;
  }

  return children;
};

const Layout = () => (
  <>
    <TopNavBar />
    <Outlet />
  </>
);

const AppRouter = () => {
  return (
    <Router>
      <Suspense fallback={
        <div className="hero min-h-screen bg-base-200">
          <div className="hero-content text-center">
            <span className="loading loading-spinner loading-lg"></span>
          </div>
        </div>
      }>
        <Routes>
          <Route path="/auth" element={<AuthPage />} />
          <Route path="/select-project" element={<ProjectSelectorPage />} />
          <Route element={<Layout />}>
            <Route path="/" element={<PrivateRoute><InfluencersPage /></PrivateRoute>} />
            <Route path="/influencers" element={<PrivateRoute><InfluencersPage /></PrivateRoute>} />
            <Route path="/projects" element={<PrivateRoute><ProjectsPage /></PrivateRoute>} />
            <Route path="/contents" element={<PrivateRoute><ContentsPage /></PrivateRoute>} />
            <Route path="/content/:id" element={<PrivateRoute><ContentPage /></PrivateRoute>} />
          </Route>
        </Routes>
      </Suspense>
    </Router>
  );
};

export default AppRouter;
