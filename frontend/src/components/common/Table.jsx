import React, { useState, useMemo, useCallback } from 'react';
import { ChevronUp, ChevronDown, ChevronsLeft, ChevronLeft, ChevronRight, ChevronsRight, Search } from 'lucide-react';
import debounce from 'lodash/debounce';

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
  const [loadingRows, setLoadingRows] = useState({});

  const handleSort = useCallback((column) => {
    if (sortColumn === column) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortColumn(column);
      setSortDirection('asc');
    }
  };

  const debouncedSearch = useMemo(
    () =>
      debounce((value) => {
        setSearchTerm(value);
        setCurrentPage(1);
      }, 300),
    []
  );

  const handleSearch = (event) => {
    debouncedSearch(event.target.value);
  };

  const handleRowSelect = useCallback((id) => {
    setSelectedRows((prev) =>
      prev.includes(id) ? prev.filter((rowId) => rowId !== id) : [...prev, id]
    );
  };

  const filteredAndSortedData = useMemo(() => {
    let result = showSearch
      ? data.filter((row) =>
          Object.values(row).some((value) =>
            value.toString().toLowerCase().includes(searchTerm.toLowerCase())
          )
        )
      : data;

    if (sortColumn) {
      result.sort((a, b) => {
        const aValue = a[sortColumn];
        const bValue = b[sortColumn];
        if (aValue < bValue) return sortDirection === 'asc' ? -1 : 1;
        if (aValue > bValue) return sortDirection === 'asc' ? 1 : -1;
        return 0;
      });
    }

    return result;
  }, [data, showSearch, searchTerm, sortColumn, sortDirection]);

  const totalPages = Math.ceil(filteredAndSortedData.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentData = filteredAndSortedData.slice(startIndex, endIndex);

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
        <div className="mb-4 w-full">
          <div className="form-control w-full">
            <div className="input-group w-full">
              <input
                type="text"
                placeholder="Search..."
                className="input input-bordered flex-grow"
                value={searchTerm}
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
                className={`${onRowClick ? 'cursor-pointer hover:bg-base-200' : ''} ${
                  customClasses.tr || ''
                }`}
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
                    {loadingRows[row.id] ? (
                      <div className="loading loading-spinner loading-sm"></div>
                    ) : column.render ? (
                      column.render(row[column.key], row)
                    ) : (
                      row[column.key]
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

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

const useKeyboardNavigation = (totalPages, currentPage, setCurrentPage) => {
  React.useEffect(() => {
    const handleKeyDown = (e) => {
      switch (e.key) {
        case 'ArrowLeft':
          setCurrentPage((prev) => Math.max(prev - 1, 1));
          break;
        case 'ArrowRight':
          setCurrentPage((prev) => Math.min(prev + 1, totalPages));
          break;
        case 'Home':
          setCurrentPage(1);
          break;
        case 'End':
          setCurrentPage(totalPages);
          break;
        default:
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [totalPages, setCurrentPage]);
};

export default Table;
