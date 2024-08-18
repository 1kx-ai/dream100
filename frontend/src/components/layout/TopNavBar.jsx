import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const TopNavBar = () => {
  const [currentProjectName, setCurrentProjectName] = useState('');

  useEffect(() => {
    const projectName = localStorage.getItem('currentProjectName');
    setCurrentProjectName(projectName || 'Select Project');
  }, []);

  return (
    <div className="navbar bg-base-100">
      <div className="flex-1">
        <Link to="/" className="btn btn-ghost normal-case text-xl">Home</Link>
        <Link to="/projects" className="btn btn-ghost normal-case text-xl">Projects</Link>
        <Link to="/influencers" className="btn btn-ghost normal-case text-xl">Influencers</Link>
      </div>
      <div className="flex-none">
        <Link to="/select-project" className="btn btn-primary">
          {currentProjectName}
        </Link>
      </div>
    </div>
  );
};

export default TopNavBar;