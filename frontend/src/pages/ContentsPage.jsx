import React, { useState, useEffect, useCallback } from 'react';
import { contentsApi } from '../services/contentsApi';
import Table from '../components/common/Table';
import SearchInput from '../components/common/SearchInput';
import { Link } from 'react-router-dom';

const ContentsPage = () => {
  const [contents, setContents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalItems, setTotalItems] = useState(0);
  const [sortColumn, setSortColumn] = useState('id');
  const [sortDirection, setSortDirection] = useState('asc');
  const [currentProjectId, setCurrentProjectId] = useState(null);
  const [currentProjectName, setCurrentProjectName] = useState('');
  const itemsPerPage = 10;

  useEffect(() => {
    const projectId = localStorage.getItem('currentProjectId');
    const projectName = localStorage.getItem('currentProjectName');
    setCurrentProjectId(projectId ? parseInt(projectId) : null);
    setCurrentProjectName(projectName || 'All Projects');
  }, []);

  const fetchContents = useCallback(async () => {
    try {
      setIsLoading(true);
      const response = await contentsApi.searchContents(
        searchQuery,
        itemsPerPage,
        (currentPage - 1) * itemsPerPage,
        sortColumn,
        sortDirection,
        currentProjectId
      );
      const data = response.contents.map(({ content, distance }) => {
        content.relevance = (1 - (distance / 2))
        content.content_preview = content.scraped_content.slice(0, 250);
        return content
      })
      setContents(data);
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
    { key: 'link', label: 'Url' },
    { key: 'content_preview', label: 'Content' },
    { key: 'relevance', label: 'Relevance' },
    {
      key: 'actions',
      label: 'Actions',
      render: (_, content) => (
        <div className="flex space-x-2">
          <Link to={`/content/${content.id}`} className="btn btn-primary btn-sm">View</Link>
        </div>
      ),
    },
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Contents - {currentProjectName}</h1>

      <div className="mb-4">
        <SearchInput onSearch={handleSearch} />
      </div>

      {error && <div className="alert alert-error mb-4">{error}</div>}

      <Table
        data={contents}
        columns={columns}
        totalItems={totalItems}
        currentPage={currentPage}
        itemsPerPage={itemsPerPage}
        loading={isLoading}
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
