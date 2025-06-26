const stats = [
    { name: 'Total Letters Generated', stat: '86' },
    { name: 'Last 14 Days', stat: '8' },
    { name: 'Estimated Hours Saved', stat: '45' },
  ]
  
  export default function Stats() {
    return (
      <div>
        <h3 className="text-base font-semibold text-gray-900">Stats</h3>
        <dl className="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-3">
          {stats.map((item) => (
            <div key={item.name} className="overflow-hidden rounded-lg bg-white px-4 py-5 shadow-md sm:p-6">
              <dt className="truncate text-sm font-medium text-gray-500">{item.name}</dt>
              <dd className="mt-1 text-3xl font-semibold tracking-tight text-gray-900">{item.stat}</dd>
            </div>
          ))}
        </dl>
      </div>
    )
  }
  