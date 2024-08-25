import { api } from './api';

export const contentsApi = {
  searchContents: (query, perPage = 10, page = 0, sortColumn = 'id', sortDirection = 'asc', projectId = null) => {
    let url = `/contents/search?query=${encodeURIComponent(query)}&per_page=${perPage}&page=${page}&sort=${sortColumn}&direction=${sortDirection}`;
    
    if (projectId !== null) {
      url += `&project_id=${projectId}`;
    }
    
    return api.get(url);
  },
  getContent: (contentId) => {
    return api.get(`/content/${contentId}`);
  },
};
