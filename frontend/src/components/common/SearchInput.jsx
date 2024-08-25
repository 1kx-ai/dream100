import React, { useState, useRef } from 'react';
import { Search } from 'lucide-react';

const SearchInput = ({ onSearch }) => {
  const [searchValue, setSearchValue] = useState('');
  const searchInputRef = useRef(null);

  const handleSearch = (event) => {
    const value = event.target.value;
    setSearchValue(value);
    onSearch(value);
  };

  const handleSearchBlur = () => {
    if (searchInputRef.current) {
      searchInputRef.current.focus();
    }
  };

  return (
    <div className="form-control w-full">
      <div className="input-group w-full">
        <input
          ref={searchInputRef}
          type="text"
          placeholder="Search..."
          className="input input-bordered flex-grow"
          value={searchValue}
          onChange={handleSearch}
          onBlur={handleSearchBlur}
        />
        <button className="btn">
          <Search size={20} />
        </button>
      </div>
    </div>
  );
};

export default SearchInput;
