import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { projectsApi } from '../services/projectsApi';

const ProjectSelectorPage = () => {
  const [projects, setProjects] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      setIsLoading(true);
      const response = await projectsApi.getProjects();
      setProjects(response);
    } catch (err) {
      console.error('Error fetching projects:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleProjectSelect = (projectId) => {
    localStorage.setItem('currentProjectId', projectId.toString());
    localStorage.setItem('currentProjectName', projects.find(p => p.id === projectId).name);
    navigate(-1); // This navigates back to the previous page
  };

  if (isLoading) {
    return (
      <div className="hero min-h-screen bg-base-200">
        <div className="hero-content text-center">
          <span className="loading loading-spinner loading-lg"></span>
        </div>
      </div>
    );
  }

  return (
    <div className="hero min-h-screen bg-base-200">
      <div className="hero-content text-center">
        <div className="max-w-md">
          <h1 className="text-5xl font-bold mb-8">Select a Project</h1>
          <ul className="menu bg-base-100 w-full rounded-box shadow-lg">
            {projects.map((project) => (
              <li key={project.id}>
                <a
                  onClick={() => handleProjectSelect(project.id)}
                  className="text-lg py-4 hover:bg-base-300 transition-colors duration-200"
                >
                  <span className="font-semibold">{project.name}</span>
                  {project.description && (
                    <span className="text-sm text-base-content text-opacity-70 mt-1">
                      {project.description}
                    </span>
                  )}
                </a>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ProjectSelectorPage;