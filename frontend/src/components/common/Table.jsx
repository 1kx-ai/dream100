import React, { useState, useCallback } from 'react';
import { ChevronUp, ChevronDown, ChevronsLeft, ChevronLeft, ChevronRight, ChevronsRight, Search } from 'lucide-react';

const Table = ({
  data,
  columns,
  totalItems,
  currentPage,
  itemsPerPage,
  onRowClick,
  customClasses = {},
  loading = false,
  showSearch = true,
  onSearch,
  onSort,
  onPageChange,
}) => {
  print(data)
  const [sortColumn, setSortColumn] = useState(null);
  const [sortDirection, setSortDirection] = useState('asc');
  const [selectedRows, setSelectedRows] = useState([]);

  const handleSort = useCallback((column) => {
    const newDirection = sortColumn === column && sortDirection === 'asc' ? 'desc' : 'asc';
    setSortColumn(column);
    setSortDirection(newDirection);
    onSort(column, newDirection);
  }, [sortColumn, sortDirection, onSort]);

  const handleSearch = (event) => {
    const value = event.target.value;
    onSearch(value);
  };

  const handleRowSelect = useCallback((id) => {
    setSelectedRows((prev) =>
      prev.includes(id) ? prev.filter((rowId) => rowId !== id) : [...prev, id]
    );
  }, []);

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

  print(data)

  if (data?.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-xl text-gray-500">No data available</p>
      </div>
    );
  }

  const totalPages = Math.ceil(totalItems / itemsPerPage);

  return (
    <div className={`overflow-x-auto ${customClasses.wrapper || ''}`}>
      {showSearch && (
        <div className="mb-4 w-full">
          <div className="form-control w-full">
            <div className="input-group w-full">
              <input
                type="text"
                placeholder="Search..."
                className="input input-bordered flex-grow"
                onChange={handleSearch}
              />
              <button className="btn">
                <Search size={20} />
              </button>
            </div>
          </div>
        </div>
      )}
      <div className="overflow-x-auto">
        <table className={`table table-zebra w-full ${customClasses.table || ''}`}>
          <thead>
            <tr>
              <th className="w-10">
                <label>
                  <input
                    type="checkbox"
                    className="checkbox"
                    checked={selectedRows.length === data?.length}
                    onChange={() =>
                      setSelectedRows(
                        selectedRows.length === data?.length
                          ? []
                          : data?.map((row) => row.id)
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
            {data?.map((row) => (
              <tr
                key={row.id}
                onClick={() => onRowClick && onRowClick(row)}
                className={`${onRowClick ? 'cursor-pointer hover:bg-base-200' : ''} ${customClasses.tr || ''}`}
              >
                <td className="w-10">
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
      </div>

      <div className="flex justify-between items-center mt-4">
        <span className="text-sm">
          Showing {(currentPage - 1) * itemsPerPage + 1} to {Math.min(currentPage * itemsPerPage, totalItems)} of {totalItems} entries
        </span>
        <div className="btn-group">
          <button
            className="btn btn-sm"
            onClick={() => onPageChange(1)}
            disabled={currentPage === 1}
          >
            <ChevronsLeft size={16} />
          </button>
          <button
            className="btn btn-sm"
            onClick={() => onPageChange(currentPage - 1)}
            disabled={currentPage === 1}
          >
            <ChevronLeft size={16} />
          </button>
          <button className="btn btn-sm">Page {currentPage} of {totalPages}</button>
          <button
            className="btn btn-sm"
            onClick={() => onPageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
          >
            <ChevronRight size={16} />
          </button>
          <button
            className="btn btn-sm"
            onClick={() => onPageChange(totalPages)}
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
