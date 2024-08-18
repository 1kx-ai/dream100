import React, { useState } from 'react';
import { ChevronUp, ChevronDown, ChevronsLeft, ChevronLeft, ChevronRight, ChevronsRight, Search } from 'lucide-react';

const Table = ({
  data,
  columns,
  itemsPerPage = 10,
  onRowClick,
  customClasses = {},
  loading = false,
  showSearch = true, // New prop to control search bar visibility
}) => {
  const [sortColumn, setSortColumn] = useState(null);
  const [sortDirection, setSortDirection] = useState('asc');
  const [currentPage, setCurrentPage] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRows, setSelectedRows] = useState([]);

  const handleSort = (column) => {
    if (sortColumn === column) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortColumn(column);
      setSortDirection('asc');
    }
  };

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
    setCurrentPage(1);
  };

  const handleRowSelect = (id) => {
    setSelectedRows((prev) =>
      prev.includes(id) ? prev.filter((rowId) => rowId !== id) : [...prev, id]
    );
  };

  const filteredData = showSearch
    ? data.filter((row) =>
      Object.values(row).some((value) =>
        value.toString().toLowerCase().includes(searchTerm.toLowerCase())
      )
    )
    : data;

  const sortedData = [...filteredData].sort((a, b) => {
    if (!sortColumn) return 0;
    const aValue = a[sortColumn];
    const bValue = b[sortColumn];
    if (aValue < bValue) return sortDirection === 'asc' ? -1 : 1;
    if (aValue > bValue) return sortDirection === 'asc' ? 1 : -1;
    return 0;
  });

  const totalPages = Math.ceil(sortedData.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentData = sortedData.slice(startIndex, endIndex);

  const renderSortIcon = (column) => {
    if (sortColumn !== column) return null;
    return sortDirection === 'asc' ? <ChevronUp size={16} /> : <ChevronDown size={16} />;
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="loading loading-spinner loading-lg"></div>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-xl text-gray-500">No data available</p>
      </div>
    );
  }

  return (
    <div className={`overflow-x-auto ${customClasses.wrapper || ''}`}>
      {showSearch && (
        <div className="mb-4">
          <div className="form-control">
            <div className="input-group">
              <input
                type="text"
                placeholder="Search..."
                className="input input-bordered"
                value={searchTerm}
                onChange={handleSearch}
              />
              <button className="btn btn-square">
                <Search size={20} />
              </button>
            </div>
          </div>
        </div>
      )}
      <table className={`table table-zebra w-full ${customClasses.table || ''}`}>
        <thead>
          <tr>
            <th>
              <label>
                <input
                  type="checkbox"
                  className="checkbox"
                  checked={selectedRows.length === currentData.length}
                  onChange={() =>
                    setSelectedRows(
                      selectedRows.length === currentData.length
                        ? []
                        : currentData.map((row) => row.id)
                    )
                  }
                />
              </label>
            </th>
            {columns.map((column) => (
              <th
                key={column.key}
                onClick={() => handleSort(column.key)}
                className={`cursor-pointer hover:bg-base-200 ${customClasses.th || ''}`}
              >
                <div className="flex items-center">
                  {column.label}
                  {renderSortIcon(column.key)}
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {currentData.map((row) => (
            <tr
              key={row.id}
              onClick={() => onRowClick && onRowClick(row)}
              className={`${onRowClick ? 'cursor-pointer hover:bg-base-200' : ''} ${customClasses.tr || ''
                }`}
            >
              <td>
                <label>
                  <input
                    type="checkbox"
                    className="checkbox"
                    checked={selectedRows.includes(row.id)}
                    onChange={() => handleRowSelect(row.id)}
                    onClick={(e) => e.stopPropagation()}
                  />
                </label>
              </td>
              {columns.map((column) => (
                <td key={column.key} className={customClasses.td || ''}>
                  {column.render ? column.render(row[column.key], row) : row[column.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      <div className="flex justify-between items-center mt-4">
        <span className="text-sm">
          Showing {startIndex + 1} to {Math.min(endIndex, sortedData.length)} of {sortedData.length} entries
        </span>
        <div className="btn-group">
          <button
            className="btn btn-sm"
            onClick={() => setCurrentPage(1)}
            disabled={currentPage === 1}
          >
            <ChevronsLeft size={16} />
          </button>
          <button
            className="btn btn-sm"
            onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
            disabled={currentPage === 1}
          >
            <ChevronLeft size={16} />
          </button>
          <button className="btn btn-sm">Page {currentPage} of {totalPages}</button>
          <button
            className="btn btn-sm"
            onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
            disabled={currentPage === totalPages}
          >
            <ChevronRight size={16} />
          </button>
          <button
            className="btn btn-sm"
            onClick={() => setCurrentPage(totalPages)}
            disabled={currentPage === totalPages}
          >
            <ChevronsRight size={16} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Table;