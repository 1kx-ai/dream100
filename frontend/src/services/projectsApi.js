import { api } from "./api";

export const projectsApi = {
  getProjects: () => api.get('/projects'),
  createProject: (projectData) => api.post('/projects', projectData),
  updateProject: (projectId, projectData) => api.put(`/projects/${projectId}`, projectData),
  deleteProject: (projectId) => api.delete(`/projects/${projectId}`)
};