// pages/Movie.tsx
import React from 'react';
import ClassRecommendationTable from '@/components/FoodsDrinksRecommendationTable';

const Movie: React.FC = () => {
  return (
    <div className="flex flex-col items-center mt-10 pt-10">
      <h1 className="text-4xl font-bold mb-6">Foods & Drinks Recommendation</h1>

      <div className="flex space-x-4 pt-4">
        <a href="/dashboard" className="bg-blue-500 text-white py-2 px-4 rounded">Manajemen Edutech</a>
        <a href="/dashboard/recommendation" className="bg-green-500 text-white py-2 px-4 rounded">Recommendation</a>
        <a href="/dashboard/movie" className="bg-yellow-500 text-white py-2 px-4 rounded">Foods & Drinks</a>
      </div>

      <div className="mt-8 w-5/6 pt-4">
        <h2 className="flex text-2xl font-bold mb-4 justify-center items-center">Foods & Drinks Recommendations Table</h2>
          <ClassRecommendationTable />
      </div>
    </div>
  );
};

export default Movie;