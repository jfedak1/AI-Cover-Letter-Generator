

export default function GettingStarted() {
    return (
      <div className="bg-white shadow-md rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-base font-semibold text-gray-900">Getting Started</h3>
          <div className="mt-2 max-w-xl text-sm text-gray-500">
            <p>
              Fill out your work profile to get started
            </p>
          </div>
          <div className="mt-5">
            <button
              type="button"
              className="cursor-pointer inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-xs hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-500"
            >
              Fill out work profile
            </button>
          </div>
        </div>
      </div>
    )
  }
  