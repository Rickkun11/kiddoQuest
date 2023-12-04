// pages/Recommendation.tsx
import React from 'react';
import ClassRecommendationTable from '@/components/ClassRecommendationTable';
import InstructorRecommendationTable from '@/components/InstructorRecommendationTable';

const Recommendation: React.FC = () => {
  return (
    <div className="flex flex-col items-center mt-10 pt-10">
      <h1 className="text-4xl font-bold mb-6">Rekomendasi Konten</h1>

      <div className="flex space-x-4 pt-4">
        <a href="/dashboard" className="bg-blue-500 text-white py-2 px-4 rounded">Manajemen Edutech</a>
        <a href="/dashboard/recommendation" className="bg-green-500 text-white py-2 px-4 rounded">Recommendation</a>
        <a href="/dashboard/movie" className="bg-yellow-500 text-white py-2 px-4 rounded">Foods & Drinks</a>
      </div>

      <div className="mt-8 w-5/6 pt-4">
        {/* Konten spesifik untuk halaman Recommendation */}
          <ClassRecommendationTable />
          <InstructorRecommendationTable />
        {/* Tambahkan lebih banyak konten spesifik recommendation sesuai kebutuhan */}
      </div>
    </div>
  );
};
export default Recommendation;