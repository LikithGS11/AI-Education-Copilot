/**
 * Tabs component for switching between different content types
 */

const Tabs = ({ tabs, activeTab, onTabChange }) => {
  if (!tabs || tabs.length === 0) return null;

  return (
    <div className="border-b border-gray-200 bg-white">
      <div className="flex gap-1 px-4">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
              activeTab === tab.id
                ? 'border-primary-600 text-primary-600'
                : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Tabs;

