import React, { useState, useEffect, useCallback } from 'react';
import { contentsApi } from '../services/contentsApi';
import Table from '../components/common/Table';

const ContentsPage = () => {
  const [contents, setContents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalItems, setTotalItems] = useState(0);
  const [sortColumn, setSortColumn] = useState('id');
  const [sortDirection, setSortDirection] = useState('asc');
  const itemsPerPage = 10;

  const fetchContents = useCallback(async () => {
    try {
      setIsLoading(true);
      const response = await contentsApi.searchContents(searchQuery, itemsPerPage, (currentPage - 1) * itemsPerPage, sortColumn, sortDirection);
      setContents(response.results);
      setTotalItems(response.count);
      setError(null);
    } catch (err) {
      setError('Failed to fetch contents. Please try again later.');
      console.error('Error fetching contents:', err);
    } finally {
      setIsLoading(false);
    }
  }, [searchQuery, currentPage, sortColumn, sortDirection]);

  useEffect(() => {
    fetchContents();
  }, [fetchContents]);

  const handleSearch = (query) => {
    setSearchQuery(query);
    setCurrentPage(1);
  };

  const handleSort = (column, direction) => {
    setSortColumn(column);
    setSortDirection(direction);
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
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
        totalItems={totalItems}
        currentPage={currentPage}
        itemsPerPage={itemsPerPage}
        loading={isLoading}
        showSearch={true}
        onSearch={handleSearch}
        onSort={handleSort}
        onPageChange={handlePageChange}
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
