import React, { useState, useEffect } from 'react';
import MainPageLayout from '../layouts/MainPageLayout';
import Modal from '../components/common/Modal';
import ProjectForm from '../components/projects/ProjectsForm';
import { projectsApi } from '../services/projectsApi';

const ProjectsPage = () => {
  const [projects, setProjects] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingProject, setEditingProject] = useState(null);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      setIsLoading(true);
      const response = await projectsApi.getProjects();
      setProjects(response);
      setError(null);
    } catch (err) {
      setError('Failed to fetch projects. Please try again later.');
      console.error('Error fetching projects:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddNew = () => {
    setEditingProject(null);
    setIsModalOpen(true);
  };

  const handleEdit = (project) => {
    setEditingProject(project);
    setIsModalOpen(true);
  };

  const handleDelete = async (id) => {
    try {
      await projectsApi.deleteProject(id);
      setProjects(projects.filter(proj => proj.id !== id));
    } catch (err) {
      setError('Failed to delete project. Please try again.');
      console.error('Error deleting project:', err);
    }
  };

  const handleSubmit = async (projectData) => {
    try {
      let response;
      if (editingProject) {
        response = await projectsApi.updateProject(editingProject.id, projectData);
        setProjects(projects.map(proj => proj.id === editingProject.id ? response : proj));
      } else {
        response = await projectsApi.createProject(projectData);
        setProjects([...projects, response]);
      }
      setIsModalOpen(false);
    } catch (err) {
      setError(`Failed to ${editingProject ? 'update' : 'add'} project. Please try again.`);
      console.error(`Error ${editingProject ? 'updating' : 'adding'} project:`, err);
    }
  };

  const renderProject = (project) => (
    <>
      <h2 className="card-title">{project.name}</h2>
      <p className="text-sm opacity-70">{project.description}</p>
      <div className="card-actions justify-end mt-4">
        <button className="btn btn-primary btn-sm" onClick={() => handleEdit(project)}>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4 mr-1">
            <path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
          </svg>
          Edit
        </button>
        <button className="btn btn-ghost btn-sm" onClick={() => handleDelete(project.id)}>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4 mr-1">
            <path strokeLinecap="round" strokeLinejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
          </svg>
          Delete
        </button>
      </div>
    </>
  );

  if (isLoading) {
    return <div className="flex justify-center items-center h-screen"><span className="loading loading-spinner loading-lg"></span></div>;
  }

  if (error) {
    return <div className="alert alert-error">{error}</div>;
  }

  return (
    <>
      <MainPageLayout
        title="Projects"
        records={projects}
        onAddNew={handleAddNew}
        renderRecord={renderProject}
      />
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingProject ? 'Edit Project' : 'Add New Project'}
      >
        <ProjectForm
          onSubmit={handleSubmit}
          initialData={editingProject}
        />
      </Modal>
    </>
  );
};

export default ProjectsPage;