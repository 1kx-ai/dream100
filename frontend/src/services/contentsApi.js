import { api } from './api';

export const contentsApi = {
  searchContents: (query, limit = 10, offset = 0, sortColumn = 'id', sortDirection = 'asc') => {
    const url = `/contents/search?query=${encodeURIComponent(query)}&limit=${limit}&offset=${offset}&sort=${sortColumn}&direction=${sortDirection}`;
    return api.get(url);
  },
};
