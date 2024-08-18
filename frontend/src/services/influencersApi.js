import { api } from './api';

export const influencersApi = {
  getInfluencers: (projectId = null) => {
    const url = projectId ? `/influencers?project_id=${projectId}` : '/influencers';
    return api.get(url);
  },
  createInfluencer: (influencerData) => api.post('/influencers', influencerData),
  updateInfluencer: (influencerId, influencerData) => api.put(`/influencers/${influencerId}`, influencerData),
  deleteInfluencer: (influencerId) => api.delete(`/influencers/${influencerId}`)
};