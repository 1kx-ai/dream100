import { api } from './api';

export const influencersApi = {
  getInfluencers: () => api.get('/influencers'),
  createInfluencer: (influencerData) => api.post('/influencers', influencerData),
  updateInfluencer: (influencerId, influencerData) => api.put(`/influencers/${influencerId}`, influencerData),
  deleteInfluencer: (influencerId) => api.delete(`/influencers/${influencerId}`)
};