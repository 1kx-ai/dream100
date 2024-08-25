import React, { useState, useEffect, useCallback } from 'react';
import { contentsApi } from '../services/contentsApi';
import Table from '../components/common/Table';

const ContentsPage = () => {
  const [contents, setContents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  const fetchContents = useCallback(async (query) => {
    try {
      setIsLoading(true);
      const response = await contentsApi.searchContents(query);
      setContents(response.results);
      setError(null);
    } catch (err) {
      setError('Failed to fetch contents. Please try again later.');
      console.error('Error fetching contents:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchContents(searchQuery);
  }, [fetchContents, searchQuery]);

  const handleSearch = (query) => {
    setSearchQuery(query);
  };

  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'title', label: 'Title' },
    { key: 'content_type', label: 'Type' },
    { key: 'created_at', label: 'Created At' },
    {
      key: 'actions',
      label: 'Actions',
      render: (_, content) => (
        <div className="flex space-x-2">
          <button className="btn btn-primary btn-sm">View</button>
        </div>
      ),
    },
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Contents</h1>

      {error && <div className="alert alert-error mb-4">{error}</div>}

      <Table
        data={contents}
        columns={columns}
        itemsPerPage={10}
        loading={isLoading}
        showSearch={true}
        onSearch={handleSearch}
        customClasses={{
          wrapper: 'shadow-lg',
          table: 'table-zebra',
          th: 'bg-primary text-primary-content',
          td: 'bg-base-100',
        }}
      />
    </div>
  );
};

export default ContentsPage;
