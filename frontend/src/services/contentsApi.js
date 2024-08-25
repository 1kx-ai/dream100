import { api } from './api';

export const contentsApi = {
  searchContents: (query, perPage = 10, page = 0, sortColumn = 'id', sortDirection = 'asc') => {
    const url = `/contents/search?query=${encodeURIComponent(query)}&perPage=${perPage}&page=${page}&sort=${sortColumn}&direction=${sortDirection}`;
    return api.get(url);
  },
};
