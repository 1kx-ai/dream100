import { api } from './api';

export const contentsApi = {
  search_contents: (query, limit = 10, offset = 0) => {
    const url = `/contents/search?query=${encodeURIComponent(query)}&limit=${limit}&offset=${offset}`
    return api.get(url);

  },
}; 