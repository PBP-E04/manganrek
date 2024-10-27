import React, { useState } from 'react';
import { Search } from 'lucide-react';

const SearchBar = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      const response = await fetch(`/promo_diskon/search/?q=${encodeURIComponent(query)}`);
      const data = await response.json();
      // Parse the serialized data
      const parsedResults = JSON.parse(data.results);
      setResults(parsedResults);
    } catch (error) {
      console.error('Error searching promos:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="mb-8">
      <form onSubmit={handleSearch} className="flex gap-2 mb-4">
        <div className="relative flex-1">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Cari promo berdasarkan kode voucher atau nama restoran..."
            className="w-full px-4 py-2 pl-10 bg-white/90 backdrop-blur-sm rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-4 h-4" />
        </div>
        <button
          type="submit"
          className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50"
          disabled={isLoading}
        >
          {isLoading ? 'Mencari...' : 'Cari'}
        </button>
      </form>

      {results.length > 0 && (
        <div className="bg-white/90 backdrop-blur-sm rounded-lg p-4">
          <h2 className="text-lg font-semibold mb-3">Hasil Pencarian</h2>
          <div className="grid gap-4">
            {results.map((result) => (
              <div
                key={result.pk}
                className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50"
              >
                <h3 className="font-semibold">{result.fields.resto}</h3>
                <p className="text-sm text-gray-600">Kode: {result.fields.kode_voucher}</p>
                <p className="text-sm text-gray-600">Diskon: {result.fields.persentase_diskon}%</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchBar;